"""The model definition for scores."""

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from apps.managers.cache_mgr import cache_mgr


class ScoreSetting(models.Model):
    """score settings models."""

    name = models.CharField(default="Score Settings",
                            max_length="30", editable=False,
                            help_text="The settings label.")
    setup_points = models.IntegerField(
        default=5,
        help_text="The point amount for setting up the profile."
    )
    active_threshold_points = models.IntegerField(
        default=50,
        help_text="The point amount for considering an active participant. It is also the "
                  "threshold point amount for awarding referral bonus.",
    )
    signup_bonus_points = models.IntegerField(
        default=2,
        help_text="The point amount for signing up a commitment or event/excursion."
    )
    quest_bonus_points = models.IntegerField(
        default=0,
        help_text="The point amount for completing a quest."
    )
    noshow_penalty_points = models.IntegerField(
        default=2,
        help_text="The point amount for no show penalty."
    )
    feedback_bonus_points = models.IntegerField(
        default=0,
        help_text="The point amount for providing action feedback."
    )
    admin_tool_tip = "The points awarded for completing various " + \
        "actions and how many points are needed for a player to be 'active'."

    class Meta:
        """meta"""
        verbose_name = "point rubric"

    def __unicode__(self):
        return "point rubric"

    def save(self, *args, **kwargs):
        """Custom save method."""
        super(ScoreSetting, self).save(*args, **kwargs)
        cache_mgr.delete("score_setting")


class ReferralSetting(models.Model):
    """Defines the model of the dynamic referral settings."""
    normal_referral_points = models.IntegerField(
        default=10,
        help_text="The point amount for normal referral bonus.",
    )
    super_referral_points = models.IntegerField(
        default=20,
        help_text="The point amount for supper referral bonus, when the referral is from a team "
                  "of participation rate from 20% to 40%",
    )
    mega_referral_points = models.IntegerField(
        default=30,
        help_text="The point amount for mega referral bonus, when the referrals is from a team of"
                  " participation rate les than 20%",
    )
    start_dynamic_bonus = models.BooleanField(
        default=False,
        help_text="Start rewarding the dynamic referral bonus. set it to true if you want to "
                  "reward referral bonus depends on referral's team participation."
    )

    def save(self, *args, **kwargs):
        """Custom save method."""
        super(ReferralSetting, self).save(*args, **kwargs)
        cache_mgr.delete("referral_setting")


class ScoreboardEntry(models.Model):
    """Defines the model that tracks user scores."""

    profile = models.ForeignKey("player_mgr.Profile", editable=False)
    round_name = models.CharField(
        max_length="30", editable=False,
        help_text="The name of the round")
    points = models.IntegerField(
        default=0,
        help_text="Points for this round")
    last_awarded_submission = models.DateTimeField(
        null=True, blank=True, editable=False,
        help_text="Last award time")

    class Meta:
        """meta"""
        unique_together = (("profile", "round_name",),)
        ordering = ("round_name",)


class PointsTransaction(models.Model):
    """Entries that track points awarded to users."""

    user = models.ForeignKey(User)
    points = models.IntegerField(
        help_text="The points for the transaction. negative number indicates a subtraction"
    )
    transaction_date = models.DateTimeField(
        help_text="The date of the transaction"
    )
    message = models.CharField(
        max_length=255,
        help_text="The message of the transcation.")

    object_id = models.PositiveIntegerField(null=True)
    content_type = models.ForeignKey(ContentType, null=True)
    related_object = generic.GenericForeignKey("content_type", "object_id")

    class Meta:
        """meta"""
        unique_together = (("user", "transaction_date", "message",),)
        ordering = ("-transaction_date",)
