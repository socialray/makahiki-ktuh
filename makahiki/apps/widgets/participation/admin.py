"""Administrator interface to score_mgr."""
from django.contrib import admin
from apps.managers.challenge_mgr import challenge_mgr
from apps.widgets.participation.models import ParticipationSetting, TeamParticipation


class ParticipationSettingAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["points_50_percent", "points_75_percent", "points_100_percent", ]


admin.site.register(ParticipationSetting, ParticipationSettingAdmin)
challenge_mgr.register_game_admin_model("participation", ParticipationSetting)


class TeamParticipationAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["team", "participation", "updated_at"]


admin.site.register(TeamParticipation, TeamParticipationAdmin)
challenge_mgr.register_game_admin_model("participation", TeamParticipation)
