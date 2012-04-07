"""The model for the energy scoreboard."""
from django.db import models

from apps.managers.team_mgr.models import Team


class EnergyData(models.Model):
    """Energy Scoreboard data model."""
    team = models.ForeignKey(Team)
    date = models.DateField()
    energy = models.IntegerField(default=0)

    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(editable=False, auto_now=True)
