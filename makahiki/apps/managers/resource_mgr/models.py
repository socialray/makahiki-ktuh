"""The model for the resource manager."""
from django.db import models

from apps.managers.team_mgr.models import Team


class ResourceSettings(models.Model):
    """resource settings model."""

    RESOURCE_CHOICE = (
        ("energy", "energy"),
        ("water", "water"),
        ("waste", "waste"),)
    WINNING_ORDER_CHOICE = (
        ("Ascending", "Ascending"),
        ("Descending", "Descending"),)

    name = models.CharField(
        choices=RESOURCE_CHOICE,
        max_length=20,
        help_text="The name of the resource.",
    )
    unit = models.CharField(
        max_length=20,
        help_text="The unit of the resource, such as kWh, Gallon, etc.",
    )
    winning_order = models.CharField(
        max_length=10,
        choices=WINNING_ORDER_CHOICE,
        help_text="The winning order.",
    )

    class Meta:
        """Meta"""
        unique_together = ("name",)


class ResourceUsage(models.Model):
    """abstract resource usage model."""
    team = models.ForeignKey(Team)
    date = models.DateField()
    time = models.TimeField()
    usage = models.IntegerField(default=0)

    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        """Meta"""
        abstract = True
        unique_together = (("date", "team",),)
        ordering = ("date", "team")


class EnergyUsage(ResourceUsage):
    """Energy usage model."""
    pass


class WaterUsage(ResourceUsage):
    """Water usage model."""
    pass


class WasteUsage(ResourceUsage):
    """Water usage model."""
    pass


class DailyResourceBaseline(models.Model):
    """Daily Team resource baseline Model for a week"""

    team = models.ForeignKey(
        Team,
        help_text="The team which this baseline is related to.")

    day = models.IntegerField(
        help_text="The day in the week, where Monday is 0 and Sunday is 6",)

    usage = models.IntegerField(
        default=0,
        help_text="The baseline energy usage of the day.",)

    updated_at = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        """Meta"""
        abstract = True
        unique_together = (("team", "day",),)
        ordering = ("team", "day")


class DailyEnergyBaseline(DailyResourceBaseline):
    """Daily Team energy baseline Model for a week"""
    pass


class DailyWaterBaseline(DailyResourceBaseline):
    """Daily Team water baseline Model for a week"""
    pass


class HourlyResourceBaseline(models.Model):
    """Daily Team resource baseline Model for a week"""

    team = models.ForeignKey(
        Team,
        help_text="The team which this baseline is related to.")

    day = models.IntegerField(
        help_text="The day in the week.",)

    hour = models.IntegerField(
        help_text="The hour in the day.",)

    usage = models.IntegerField(
        default=0,
        help_text="The baseline energy usage of the day.",)

    updated_at = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        """Meta"""
        abstract = True
        unique_together = (("team", "day", "hour"),)
        ordering = ("team", "day", "hour")


class HourlyEnergyBaseline(HourlyResourceBaseline):
    """Hourly Team energy baseline Model for a week"""
    pass


class HourlyWaterBaseline(HourlyResourceBaseline):
    """Hourly Team water baseline Model for a week"""
    pass
