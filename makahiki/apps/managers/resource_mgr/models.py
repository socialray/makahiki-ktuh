"""The model for the resource manager."""
from django.db import models

from apps.managers.team_mgr.models import Team


class ResourceSettings(models.Model):
    """resource settings model."""

    RESOURCE_CHOICE = (
        ("Energy", "Energy"),
        ("Water", "Water"),
        ("Waste", "Waste"),)
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
