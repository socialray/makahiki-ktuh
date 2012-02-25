"""
Player Manager Models
"""
import datetime

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.localflavor.us.models import PhoneNumberField
from managers.score_mgr.models import ScoreboardEntry, PointsTransaction

from managers.team_mgr.models import Team
from managers.settings_mgr import get_current_round
from managers.cache_mgr.utils import invalidate_info_bar_cache

class Profile(models.Model):
    """
    Profile represents a player's profile info, and his points, and other book keeping.
    """
    user = models.ForeignKey(User, unique=True, verbose_name='user',
        related_name='profile')
    name = models.CharField('name', unique=True, max_length=50)
    first_name = models.CharField('first_name', max_length=50, null=True,
        blank=True)
    last_name = models.CharField('last_name', max_length=50, null=True,
        blank=True)
    points = models.IntegerField(default=0, editable=False)
    last_awarded_submission = models.DateTimeField(null=True, blank=True,
        editable=False)
    team = models.ForeignKey(Team, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    contact_text = PhoneNumberField(null=True, blank=True)
    contact_carrier = models.CharField(max_length=50, null=True, blank=True)
    enable_help = models.BooleanField(default=True)
    canopy_member = models.BooleanField(default=False)
    canopy_karma = models.IntegerField(default=0, editable=False)

    # Check first login completion.
    setup_profile = models.BooleanField(default=False, editable=False)
    setup_complete = models.BooleanField(default=False, )
    completion_date = models.DateTimeField(null=True, blank=True,
        )

    # Check visits for daily visitor badge.
    daily_visit_count = models.IntegerField(default=0, editable=False)
    last_visit_date = models.DateField(null=True, blank=True)

    # Check for referrer
    referring_user = models.ForeignKey(User, null=True, blank=True,
        related_name='referred_profiles')
    referrer_awarded = models.BooleanField(default=False, editable=False)

    def __unicode__(self):
        return self.name

    @staticmethod
    def points_leaders(num_results=10, round_name=None):
        """
        Returns the top points leaders out of all users.
        """
        if round_name:
            return Profile.objects.filter(
                scoreboardentry__round_name=round_name,
            ).order_by("-scoreboardentry__points",
                "-scoreboardentry__last_awarded_submission")[:num_results]

        return Profile.objects.all().order_by("-points", "-last_awarded_submission")[:num_results]

    def current_round_points(self):
        """Returns the amount of points the user has in the current round."""
        current_round = get_current_round()
        if current_round:
            return ScoreboardEntry.objects.get(profile=self,
                round_name=current_round).points

        return self.points

    def current_round_overall_rank(self):
        """Returns the overall rank of the user for the current round."""
        current_round = get_current_round()
        if current_round:
            return self.overall_rank(round_name=current_round)

        return None

    def current_round_team_rank(self):
        """Returns the rank of the user for the current round in their own team."""
        current_round = get_current_round()
        if current_round:
            return self.team_rank(round_name=current_round)

        return None

    def team_rank(self, round_name=None):
        """Returns the rank of the user in their own team."""
        if round_name:
            return ScoreboardEntry.user_round_team_rank(self.user, round_name)

        # Calculate the rank.
        # This counts the number of people who are on the team that have more points
        # OR have the same amount of points but a later submission date
        if self.last_awarded_submission:
            return Profile.objects.filter(
                Q(points__gt=self.points) |
                Q(points=self.points,
                    last_awarded_submission__gt=self.last_awarded_submission),
                team=self.team,
                user__is_staff=False,
                user__is_superuser=False,
            ).count() + 1

        return Profile.objects.filter(
            points__gt=self.points,
            team=self.team,
            user__is_staff=False,
            user__is_superuser=False,
        ).count() + 1


    def overall_rank(self, round_name=None):
        """Returns the overall rank of the user."""
        if round_name:
            return ScoreboardEntry.user_round_overall_rank(self.user,
                round_name)

        # Compute the overall rank.  This counts the number of people that have more points
        # OR have the same amount of points but a later submission date
        if self.last_awarded_submission:
            return Profile.objects.filter(
                Q(points__gt=self.points) |
                Q(points=self.points,
                    last_awarded_submission__gt=self.last_awarded_submission),
                user__is_staff=False,
                user__is_superuser=False,
            ).count() + 1

        return Profile.objects.filter(
            points__gt=self.points,
            user__is_staff=False,
            user__is_superuser=False,
        ).count() + 1

    def canopy_karma_info(self):
        """
        Returns a dictionary containing the user's rank and the total number of canopy members.
        """
        query = Profile.objects.filter(canopy_member=True)
        return {
            "rank": query.filter(canopy_karma__gt=self.canopy_karma).count() + 1
            ,
            "total": query.count(),
            }

    def _is_canopy_activity(self, related_object):
        """check if the related_object is a canopy activity"""
        return related_object != None and\
               ((hasattr(related_object,
                   "activity") and related_object.activity.is_canopy)
                or
                (hasattr(related_object,
                    "commitment") and related_object.commitment.is_canopy))

    def add_points(self, points, submission_date, message, related_object=None):
        """
        Adds points based on the point value of the submitted object.
        Note that this method does not save the profile.
        """
        # Create a transaction first.
        transaction = PointsTransaction(
            user=self.user,
            points=points,
            submission_date=submission_date,
            message=message,
        )
        if related_object:
            transaction.related_object = related_object

        transaction.save()

        # Invalidate info bar cache.
        invalidate_info_bar_cache(self.user)

        # canopy activity deal with karma
        if self._is_canopy_activity(related_object):
            self.canopy_karma += points
        else:
            self.points += points

            if not self.last_awarded_submission or submission_date > self.last_awarded_submission:
                self.last_awarded_submission = submission_date

            current_round = self._get_round(submission_date)

            # If we have a round, then update the scoreboard entry.
            # Otherwise, this just counts towards overall.
            if current_round:
                entry, _ = ScoreboardEntry.objects.get_or_create(
                    profile=self, round_name=current_round)
                entry.points += points
                if not entry.last_awarded_submission or \
                   submission_date > entry.last_awarded_submission:
                    entry.last_awarded_submission = submission_date
                entry.save()

    def remove_points(self, points, submission_date, message,
                      related_object=None):
        """
        Removes points from the user. Note that this method does not save the profile.
        If the submission date is the same as the last_awarded_submission field, we rollback
        to a previously completed task.
        """

        # Invalidate info bar cache.
        invalidate_info_bar_cache(self.user)

        self.points -= points

        current_round = self._get_round(submission_date)
        # If we have a round, then update the scoreboard entry.
        # Otherwise, this just counts towards overall.
        if current_round:
            try:
                entry = ScoreboardEntry.objects.get(profile=self, round_name=current_round)
                entry.points -= points
                if entry.last_awarded_submission == submission_date:
                    # Need to find the previous update.
                    entry.last_awarded_submission = self._last_submitted_before(submission_date)

                entry.save()
            except ObjectDoesNotExist:
                # This should not happen once the competition is rolling.
                raise

        if self.last_awarded_submission == submission_date:
            self.last_awarded_submission = self._last_submitted_before(submission_date)

        # Log the transaction.
        transaction = PointsTransaction(
            user=self.user,
            points=points * -1,
            submission_date=submission_date,
            message=message,
        )
        if related_object:
            transaction.related_object = related_object

        transaction.save()

    def _get_round(self, submission_date):
        """Get the round that the submission date corresponds to.
        Returns None if it doesn't correspond to anything."""

        rounds = settings.COMPETITION_ROUNDS

        # Find which round this belongs to.
        for key in rounds:
            start = datetime.datetime.strptime(rounds[key]["start"], "%Y-%m-%d %H:%M:%S")
            end = datetime.datetime.strptime(rounds[key]["end"], "%Y-%m-%d %H:%M:%S")
            if submission_date >= start and submission_date < end:
                return key

        return None

    def _last_submitted_before(self, submission_date):
        """
        Time of the last task that was completed before the submission date.
        Returns None if there are no other tasks.
        """
        try:
            return PointsTransaction.objects.filter(
                user=self.user,
                submission_date__lt=submission_date).latest("submission_date").submission_date
        except ObjectDoesNotExist:
            return None

    def save(self, *args, **kwargs):
        """
        Custom save method to check for referral bonus.
        """
        has_referral = self.referring_user is not None and not self.referrer_awarded
        referrer = None
        if has_referral and self.points >= 30:
            self.referrer_awarded = True
            referrer = Profile.objects.get(user=self.referring_user)
            self.add_points(10, datetime.datetime.today(),
                'Referred by %s' % referrer.name, self)

        super(Profile, self).save(*args, **kwargs)

        if referrer:
            referrer.add_points(10, datetime.datetime.today(),
                'Referred %s' % self.name, referrer)
            referrer.save()

    class Meta:
        """ Meta
        """
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'


def create_profile(sender, instance=None, **kwargs):
    """ create a profile automatically when creating a user.
    """
    _ = sender
    if (kwargs.get('created', True) and not kwargs.get('raw', False)):
        profile, _ = Profile.objects.get_or_create(user=instance,
            name=instance.username)
        for key in settings.COMPETITION_ROUNDS.keys():
            ScoreboardEntry.objects.get_or_create(
                profile=profile, round_name=key)

post_save.connect(create_profile, sender=User)
