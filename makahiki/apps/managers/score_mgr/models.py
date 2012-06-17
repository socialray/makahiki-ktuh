"""The model definition for scores."""
from django.conf import settings

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


class ScoreSetting(models.Model):
    """score settings models."""

    setup_points = models.IntegerField(
        default=5,
        help_text="The point amount for setting up the profile."
    )
    referral_bonus_points = models.IntegerField(
        default=10,
        help_text="The point amount for referral bonus.",
    )
    active_threshold_points = models.IntegerField(
        default=50,
        help_text="The threshold point amount for active participation.It is also the threshold"
                  "for awarding referral bonus.",
    )
    signup_bonus_points = models.IntegerField(
        default=2,
        help_text="The point amount for signing up a commitment or activity."
    )
    quest_bonus_points = models.IntegerField(
        default=0,
        help_text="The point amount for completing a quest."
    )
    noshow_penalty_points = models.IntegerField(
        default=4,
        help_text="The point amount for no show penalty."
    )
    feedback_bonus_points = models.IntegerField(
        default=0,
        help_text="The point amount for providing action feedback."
    )

    def save(self, *args, **kwargs):
        """Custom save method."""
        super(ScoreSetting, self).save(*args, **kwargs)
        settings.CHALLENGE.score_setting = self


class ScoreboardEntry(models.Model):
    """Defines the model that tracks user scores."""

    profile = models.ForeignKey("player_mgr.Profile", editable=False)
    round_name = models.CharField(
        max_length="30", editable=False,
        help_text="The name of the round")
    points = models.IntegerField(
        default=0, editable=False,
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
