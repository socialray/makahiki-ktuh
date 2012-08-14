"""The model definition for scores."""

from django.db import models
from apps.managers.team_mgr.models import Team


class ParticipationSetting(models.Model):
    """participation settings models."""

    points_50_percent = models.IntegerField(
        default=5,
        help_text="The point amount for 50 percent participation."
    )
    points_75_percent = models.IntegerField(
        default=5,
        help_text="The point amount for 75 percent participation."
    )
    points_100_percent = models.IntegerField(
        default=10,
        help_text="The point amount for 100 percent participation."
    )


class TeamParticipation(models.Model):
    """participation for each team."""
    team = models.ForeignKey(
        Team,
        help_text="The team.")

    participation = models.IntegerField(
        default=0,
        help_text="The participate rate of the team.",)

    updated_at = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        """Meta"""
        ordering = ["-participation", ]
