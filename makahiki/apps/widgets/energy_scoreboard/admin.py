"""Administrator interface to energy scoreboard, display the team, date, and energy."""
from django.contrib import admin

from apps.widgets.energy_scoreboard.models import EnergyData


class EnergyDataAdmin(admin.ModelAdmin):
    """Administrator display list: team, date, and energy."""
    list_display = ["team", "date", "energy"]

admin.site.register(EnergyData, EnergyDataAdmin)
