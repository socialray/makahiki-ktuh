"""Define the model for Player state."""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.contrib.localflavor.us.models import PhoneNumberField
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.score_mgr import score_mgr
from apps.managers.team_mgr.models import Team


class Profile(models.Model):
    """Profile represents a player's profile info, and his points,
       and other book keeping.
    """
    user = models.ForeignKey(User, unique=True, verbose_name='user', related_name='profile',
                             help_text="The login user")
    name = models.CharField('name', unique=True, max_length=50,
                            help_text="The name of the player")
    first_name = models.CharField('first_name', max_length=50, null=True, blank=True,
                                  help_text="The first name of the player")
    last_name = models.CharField('last_name', max_length=50, null=True, blank=True,
                                 help_text="The last name of the player")
    team = models.ForeignKey(Team, null=True, blank=True,
                             help_text="The team of the player")
    contact_email = models.EmailField(null=True, blank=True,
                                      help_text="The contact email of the player")
    contact_text = PhoneNumberField(null=True, blank=True,
                                    help_text="The contact phone number")
    contact_carrier = models.CharField(max_length=50, null=True, blank=True,
                                       help_text="The phone carrier of the contact number")

    # Check first login completion.
    setup_profile = models.BooleanField(default=False, editable=False,
                                        help_text="Has the player's profile setup?")
    setup_complete = models.BooleanField(default=False,
                                        help_text="Has the player completed the first login?")
    completion_date = models.DateTimeField(null=True, blank=True,
                                           help_text="The date of the first login completed")

    # Check visits for daily visitor badge.
    daily_visit_count = models.IntegerField(default=0, editable=False,
                                            help_text="The number of the daily visit")
    last_visit_date = models.DateField(null=True, blank=True,
                                       help_text="The date of the last visit")

    # Check for referrer
    referring_user = models.ForeignKey(User, null=True, blank=True,
                                       related_name='referred_profiles',
                                       help_text="The referring user")
    referrer_awarded = models.BooleanField(default=False, editable=False,
                                           help_text="Has the referral bonus awarded?")

    class Meta:
        """Meta sets verbosse name and plural."""
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    def __unicode__(self):
        return self.name

    def current_round_points(self):
        """Returns the total number of points for the user.  Optional parameter for a round."""
        current_round = challenge_mgr.get_current_round()
        return score_mgr.player_points(self, round_name=current_round)

    def points(self):
        """Returns the total number of points for the user.  Optional parameter for a round."""
        return score_mgr.player_points(self)

    def last_awarded_submission(self):
        """Returns the last awarded submission date."""
        return score_mgr.player_last_awarded_submission(self)

    def current_round_overall_rank(self):
        """Returns the overall rank of the user for the current round."""
        current_round = challenge_mgr.get_current_round()
        return score_mgr.player_rank(self, round_name=current_round)

    def overall_rank(self):
        """Returns the rank of the user for the round."""
        return score_mgr.player_rank(self)

    def current_round_team_rank(self):
        """Returns the rank of the user for the current round in their own team."""
        current_round = challenge_mgr.get_current_round()
        return score_mgr.player_rank_in_team(self, round_name=current_round)

    def team_rank(self):
        """Returns the rank of the user in their own team."""
        return score_mgr.player_rank_in_team(self)

    def add_points(self, points, transaction_date, message, related_object=None):
        """Adds points based on the point value of the submitted object."""
        score_mgr.player_add_points(self, points, transaction_date, message, related_object)

    def remove_points(self, points, transaction_date, message, related_object=None):
        """Removes points from the user."""
        score_mgr.player_remove_points(self, points, transaction_date, message, related_object)

    def remove_related_points(self, related_object):
        """Removes points related to the related_object (action) from the user."""
        score_mgr.player_remove_related_points(self, related_object)


def create_profile(sender, instance=None, **kwargs):
    """ Create a profile automatically when creating a user."""
    _ = sender
    if (kwargs.get('created', True) and not kwargs.get('raw', False)):
        Profile.objects.get_or_create(user=instance, name=instance.username)


post_save.connect(create_profile, sender=User)


def award_possible_referral_bonus(sender, instance=None, **kwargs):
    """award possible referral bonus when creating profile."""
    _ = sender
    _ = kwargs
    has_referral = instance.referring_user is not None and not instance.referrer_awarded
    if has_referral and instance.points() >= score_mgr.active_threshold_points():
        instance.referrer_awarded = True
        referrer = Profile.objects.get(user=instance.referring_user)
        score_mgr.award_referral_bonus(instance, referrer)


pre_save.connect(award_possible_referral_bonus, sender=Profile)
