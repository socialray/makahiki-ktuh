"""Administrator interface to score_mgr."""
from django.contrib import admin
from apps.managers.challenge_mgr import challenge_mgr
from apps.widgets.participation.models import ParticipationSetting, TeamParticipation


class ParticipationSettingAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["name", ]
    list_display_links = ["name", ]
    page_text = "There must only be one Participation Setting.  You can edit the amount" + \
    " of points awarded per player for the various levels of team participation."

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

challenge_mgr.register_developer_game_info_model("Participation Game", ParticipationSetting)
challenge_mgr.register_developer_game_info_model("Participation Game", TeamParticipation)
