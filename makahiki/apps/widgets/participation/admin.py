"""Administrator interface to score_mgr."""
from django.contrib import admin
from apps.managers.challenge_mgr import challenge_mgr
from apps.widgets.participation.models import ParticipationSetting, TeamParticipation


class ParticipationSettingAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["points_50_percent", "points_75_percent", "points_100_percent", ]
    list_display_links = ["points_50_percent", "points_75_percent", "points_100_percent", ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(ParticipationSetting, ParticipationSettingAdmin)
challenge_mgr.register_designer_game_info_model("Participation Game", ParticipationSetting)


class TeamParticipationAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["round_name", "team", "participation", "awarded_percent", "updated_at"]
    list_filter = ["round_name"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(TeamParticipation, TeamParticipationAdmin)
