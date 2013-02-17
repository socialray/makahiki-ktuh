"""The model definition for scores."""

from django.db import models
from django.template.defaultfilters import slugify
from apps.managers.cache_mgr import cache_mgr
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.team_mgr.models import Team


class ParticipationSetting(models.Model):
    """participation settings models."""

    name = models.CharField(default="Participation Settings",
                            max_length="30", editable=False,
                            help_text="The settings label.")
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
    admin_tool_tip = "Points for different participation levels"


class TeamParticipation(models.Model):
    """participation for each team."""
    round_name = models.CharField(
        null=True, blank=True,
        help_text="The name of the round.",
        max_length=50,)

    team = models.ForeignKey(
        Team,
        help_text="The team.")

    participation = models.IntegerField(
        default=0,
        help_text="The participate rate of the team.",)

    awarded_percent = models.CharField(
        max_length=10,
        null=True, blank=True,
        help_text="The awarded percentage."
    )

    updated_at = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        """Meta"""
        ordering = ["-participation", ]

    def save(self, *args, **kwargs):
        """Custom save method."""
        super(TeamParticipation, self).save(*args, **kwargs)
        for round_name in challenge_mgr.get_all_round_info()["rounds"].keys():
            cache_mgr.delete("p_ranks-%s" % slugify(round_name))
