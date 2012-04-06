"""The model definition for scores."""

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


class ScoreboardEntry(models.Model):
    """Defines the model that tracks user scores."""

    profile = models.ForeignKey("player_mgr.Profile", editable=False)
    round_name = models.CharField(max_length="30", editable=False,
                                  help_text="The name of the round")
    points = models.IntegerField(default=0, editable=False,
                                 help_text="Points for this round")
    last_awarded_submission = models.DateTimeField(null=True, blank=True, editable=False,
                                                   help_text="Last award time")

    class Meta:
        """meta"""
        unique_together = (("profile", "round_name",),)
        ordering = ("round_name",)


class PointsTransaction(models.Model):
    """Entries that track points awarded to users."""

    user = models.ForeignKey(User)
    points = models.IntegerField()
    submission_date = models.DateTimeField()
    message = models.CharField(max_length=255)
    object_id = models.PositiveIntegerField(null=True)
    content_type = models.ForeignKey(ContentType, null=True)
    related_object = generic.GenericForeignKey("content_type", "object_id")
