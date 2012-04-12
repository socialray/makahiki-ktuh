"""The model for the resource manager."""
from django.db import models

from apps.managers.team_mgr.models import Team


class EnergyData(models.Model):
    """Energy data model."""
    team = models.ForeignKey(Team)
    date = models.DateField()
    time = models.TimeField()
    usage = models.IntegerField(default=0)

    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(editable=False, auto_now=True)


class WaterData(models.Model):
    """Water data model."""
    team = models.ForeignKey(Team)
    date = models.DateField()
    usage = models.IntegerField(default=0)

    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(editable=False, auto_now=True)
