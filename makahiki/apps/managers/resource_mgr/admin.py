"""Administrator interface to resource manager."""
from django.contrib import admin
from apps.managers.challenge_mgr import challenge_mgr

from apps.managers.resource_mgr.models import EnergyUsage, WaterUsage, ResourceSetting, \
    ResourceBlackoutDate


class UsageAdmin(admin.ModelAdmin):
    """Administrator display list: team, date, and energy."""
    list_display = ["date", "team", "time", "usage", "updated_at"]
    search_fields = ["team__name", ]
    list_filter = ['team']
    date_hierarchy = "date"

admin.site.register(EnergyUsage, UsageAdmin)
admin.site.register(WaterUsage, UsageAdmin)


class ResourceSettingsAdmin(admin.ModelAdmin):
    """Administrator display list: team, date, and energy."""
    list_display = ["name", "unit", "winning_order", "conversion_rate"]

admin.site.register(ResourceSetting, ResourceSettingsAdmin)
challenge_mgr.register_site_admin_model("Challenge", ResourceSetting)


class ResourceBlackoutDateAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["date", "description"]

admin.site.register(ResourceBlackoutDate, ResourceBlackoutDateAdmin)
challenge_mgr.register_site_admin_model("Challenge", ResourceBlackoutDate)
