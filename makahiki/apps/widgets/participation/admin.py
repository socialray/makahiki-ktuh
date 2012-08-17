"""Administrator interface to score_mgr."""
from django.contrib import admin
from apps.managers.challenge_mgr import challenge_mgr
from apps.widgets.participation.models import ParticipationSetting


class ParticipationSettingAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["points_50_percent", "points_75_percent", "points_100_percent", ]


admin.site.register(ParticipationSetting, ParticipationSettingAdmin)
challenge_mgr.register_game_admin_model("participation", ParticipationSetting)
