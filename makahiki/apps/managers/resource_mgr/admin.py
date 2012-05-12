"""Administrator interface to resource manager."""
from django.contrib import admin

from apps.managers.resource_mgr.models import EnergyUsage, WaterUsage, ResourceSettings


class UsageAdmin(admin.ModelAdmin):
    """Administrator display list: team, date, and energy."""
    list_display = ["date", "team", "time", "usage"]

admin.site.register(EnergyUsage, UsageAdmin)
admin.site.register(WaterUsage, UsageAdmin)


class ResourceSettingsAdmin(admin.ModelAdmin):
    """Administrator display list: team, date, and energy."""
    list_display = ["name", "unit", "winning_order", ]

admin.site.register(ResourceSettings, ResourceSettingsAdmin)
