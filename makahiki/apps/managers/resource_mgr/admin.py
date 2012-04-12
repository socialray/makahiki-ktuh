"""Administrator interface to energy scoreboard, display the team, date, and energy."""
from django.contrib import admin

from apps.managers.resource_mgr.models import EnergyData


class EnergyDataAdmin(admin.ModelAdmin):
    """Administrator display list: team, date, and energy."""
    list_display = ["team", "date", "time", "usage"]

admin.site.register(EnergyData, EnergyDataAdmin)
