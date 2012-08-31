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

    percent_reduction = models.IntegerField(
        default=0,
        help_text="The percentage of reduction.")

    current_goal_percent_reduction = models.IntegerField(
        default=0,
        help_text="The current goal percentage of reduction when using dynamic baseline method.")

    class Meta:
        """Meta"""
        abstract = True
        unique_together = (("team", "date",),)
        ordering = ("team", "-date")


class EnergyGoal(ResourceGoal):
    """Energy goal"""
    pass


class WaterGoal(ResourceGoal):
    """Water goal"""
    pass


class ResourceGoalSetting(models.Model):
    """Team Resource Goal Setting Model"""

    BASELINE_CHOICES = (("Dynamic", "Dynamic"),
                    ("Fixed", "Fixed"))

    team = models.ForeignKey(
        Team,
        help_text="The team which this goal is related to.")

    goal_percent_reduction = models.IntegerField(
        default=5,
        help_text="The goal percentage of reduction.")

    baseline_method = models.CharField(
        default="Dynamic",
        choices=BASELINE_CHOICES,
        max_length=20,
        help_text="The method of calculating the baseline.")

    goal_points = models.IntegerField(
        default=20,
        help_text="The amount of points to award for completing a goal.")

    manual_entry = models.BooleanField(
        default=False,
        help_text="Manually enter the data?",)

    manual_entry_time = models.TimeField(
        blank=True, null=True,
        help_text="The time for manual data entry.",)

    realtime_meter_interval = models.IntegerField(
        default=10,
        help_text="The refresh interval (in seconds) for the real-time meter display. " \
                  "not applicable when the Manual Entry is checked.")

    class Meta:
        """Meta"""
        abstract = True
        unique_together = ("team",)
        ordering = ("team",)


class EnergyGoalSetting(ResourceGoalSetting):
    """Energy goal settings."""
    pass


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
    class Meta:
        """meta"""
        verbose_name_plural = "Energy daily baselines"


class WaterBaselineDaily(ResourceBaselineDaily):
    """Daily Team water baseline Model for a week"""
    class Meta:
        """meta"""
        verbose_name_plural = "Water daily baselines"


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
    class Meta:
        """meta"""
        verbose_name_plural = "Energy Hourly baselines"


class WaterBaselineHourly(ResourceBaselineHourly):
    """Hourly Team water baseline Model for a week"""
    class Meta:
        """meta"""
        verbose_name_plural = "Water Hourly baselines"
