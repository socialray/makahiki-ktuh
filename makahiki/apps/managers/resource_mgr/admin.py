"""Administrator interface to resource manager."""
from django.contrib import admin
from apps.managers.challenge_mgr import challenge_mgr

from apps.managers.resource_mgr.models import EnergyUsage, WaterUsage, ResourceSetting, \
    ResourceBlackoutDate, WasteUsage


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
    readonly_fields = ["name"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(ResourceSetting, ResourceSettingsAdmin)
challenge_mgr.register_designer_challenge_info_model("Other Settings", 3, ResourceSetting, 5)


class ResourceBlackoutDateAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["date", "description"]

admin.site.register(ResourceBlackoutDate, ResourceBlackoutDateAdmin)
challenge_mgr.register_designer_challenge_info_model("Other Settings", 3, ResourceBlackoutDate, 4)

challenge_mgr.register_developer_challenge_info_model("Resources", 5, ResourceSetting, 1)
challenge_mgr.register_developer_challenge_info_model("Resources", 5, ResourceBlackoutDate, 1)
challenge_mgr.register_developer_game_info_model("Energy Game", EnergyUsage)
challenge_mgr.register_developer_game_info_model("Water Game", WaterUsage)
challenge_mgr.register_developer_game_info_model("Waste Game", WasteUsage)
