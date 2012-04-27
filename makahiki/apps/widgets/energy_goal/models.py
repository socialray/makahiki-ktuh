"""Energy goal model definition."""

from django.db import models

from apps.managers.team_mgr.models import Team


class EnergyGoal(models.Model):
    """Team Energy Goal Model"""
    STATUS_CHOICES = (("Over the goal", "Over the goal"),
                    ("Below the goal", "Below the goal"),
                    ("Unknown", "Unknown"),
                    ("Not available", "Not available"),)

    team = models.ForeignKey(
        Team,
        help_text="The team which this goal is related to.")

    date = models.DateField(
        help_text="The date of the month.")

    goal_status = models.CharField(
        default="Not available",
        choices=STATUS_CHOICES,
        max_length=20,
        help_text="The status of the goal.")


class EnergyGoalSettings(models.Model):
    """Team Energy Goal Model"""

    team = models.ForeignKey(
        Team,
        help_text="The team which this goal is related to.")

    goal_percent_reduction = models.IntegerField(
        default=5,
        help_text="The goal percentage of reduction.")

    warning_percent_reduction = models.IntegerField(
        default=3,
        help_text="The warning percentage of reduction.")

    goal_points = models.IntegerField(
        default=20,
        help_text="The amount of points to award for completing a goal.")

    manual_entry = models.BooleanField(
        default=False,
        help_text="Manually enter energy data?",)

    manual_entry_time = models.TimeField(
        blank=True, null=True,
        help_text="The time for manual energy data entry.",)
