"""Admin"""
from django.contrib import admin

from apps.widgets.energy_scoreboard.models import EnergyData


class EnergyDataAdmin(admin.ModelAdmin):
    """Admin"""
    list_display = ["team", "date", "energy"]

admin.site.register(EnergyData, EnergyDataAdmin)
