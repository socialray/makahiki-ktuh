"""Admin Definition"""
from django.contrib import admin

from apps.widgets.energy_power_meter.models import PowerData


class PowerDataAdmin(admin.ModelAdmin):
    """Admin"""
    list_display = ["team", "current_power", "baseline_power"]

admin.site.register(PowerData, PowerDataAdmin)
