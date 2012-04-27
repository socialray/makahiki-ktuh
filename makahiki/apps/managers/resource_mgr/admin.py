"""Administrator interface to resource manager."""
from django.contrib import admin

from apps.managers.resource_mgr.models import EnergyUsage, WaterUsage, \
    WasteUsage, ResourceSettings, HourlyEnergyBaseline, DailyEnergyBaseline


class UsageAdmin(admin.ModelAdmin):
    """Administrator display list: team, date, and energy."""
    list_display = ["date", "team", "time", "usage"]

admin.site.register(EnergyUsage, UsageAdmin)
admin.site.register(WaterUsage, UsageAdmin)
admin.site.register(WasteUsage, UsageAdmin)


class DailyEnergyBaselineAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["day", "team", "usage"]

admin.site.register(DailyEnergyBaseline, DailyEnergyBaselineAdmin)


class HourlyEnergyBaselineAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["day", "hour", "team", "usage"]

admin.site.register(HourlyEnergyBaseline, HourlyEnergyBaselineAdmin)


class ResourceSettingsAdmin(admin.ModelAdmin):
    """Administrator display list: team, date, and energy."""
    list_display = ["name", "unit", "winning_order", ]

admin.site.register(ResourceSettings, ResourceSettingsAdmin)
