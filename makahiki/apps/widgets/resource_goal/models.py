"""Energy goal model definition."""

from django.db import models

from apps.managers.team_mgr.models import Team


class ResourceGoal(models.Model):
    """Team Resource Goal Model"""
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

    class Meta:
        """Meta"""
        abstract = True
        unique_together = (("team", "date",),)
        ordering = ("team", "date")


class EnergyGoal(ResourceGoal):
    """Energy goal"""
    pass


class WaterGoal(ResourceGoal):
    """Water goal"""
    pass


class ResourceGoalSetting(models.Model):
    """Team Resource Goal Setting Model"""

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
        help_text="Manually enter the data?",)

    manual_entry_time = models.TimeField(
        blank=True, null=True,
        help_text="The time for manual data entry.",)

    class Meta:
        """Meta"""
        abstract = True
        unique_together = ("team",)
        ordering = ("team",)


class EnergyGoalSetting(ResourceGoalSetting):
    """Energy goal settings."""
    power_meter_interval = models.IntegerField(
            default=10,
            help_text="The refresh interval (in seconds) for the power meter display.")


class WaterGoalSetting(ResourceGoalSetting):
    """Water goal settings"""
    pass


class ResourceBaselineDaily(models.Model):
    """Daily Team resource baseline Model for a week"""
    DAY_CHOICES = ((0, "Monday"),
                   (1, "Tuesday"),
                   (2, "Wednesday"),
                   (3, "Thursday"),
                   (4, "Friday"),
                   (5, "Saturday"),
                   (6, "Sunday"))
    team = models.ForeignKey(
        Team,
        help_text="The team which this baseline is related to.")

    day = models.IntegerField(
        choices=DAY_CHOICES,
        help_text="The day in the week",)

    usage = models.IntegerField(
        default=0,
        help_text="The baseline usage of the day.",)

    updated_at = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        """Meta"""
        abstract = True
        unique_together = (("team", "day",),)
        ordering = ("team", "day")


class EnergyBaselineDaily(ResourceBaselineDaily):
    """Daily Team energy baseline Model for a week"""
    pass


class WaterBaselineDaily(ResourceBaselineDaily):
    """Daily Team water baseline Model for a week"""
    pass


class ResourceBaselineHourly(models.Model):
    """Daily Team resource baseline Model for a week"""

    DAY_CHOICES = ((0, "Monday"),
                   (1, "Tuesday"),
                   (2, "Wednesday"),
                   (3, "Thursday"),
                   (4, "Friday"),
                   (5, "Saturday"),
                   (6, "Sunday"))

    team = models.ForeignKey(
        Team,
        help_text="The team which this baseline is related to.")

    day = models.IntegerField(
        choices=DAY_CHOICES,
        help_text="The day in the week.",)

    hour = models.IntegerField(
        help_text="The hour in the day.",)

    usage = models.IntegerField(
        default=0,
        help_text="The baseline usage of the day.",)

    updated_at = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        """Meta"""
        abstract = True
        unique_together = (("team", "day", "hour"),)
        ordering = ("team", "day", "hour")


class EnergyBaselineHourly(ResourceBaselineHourly):
    """Hourly Team energy baseline Model for a week"""
    pass


class WaterBaselineHourly(ResourceBaselineHourly):
    """Hourly Team water baseline Model for a week"""
    pass
