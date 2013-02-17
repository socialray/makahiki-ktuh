"""Energy goal widget administrator interface; shows the team, actual vs. goal, last update."""

from django.contrib import admin
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.resource_mgr.models import WaterUsage
from apps.widgets.resource_goal.admin import GoalSettingsAdmin, GoalAdmin, BaselineDailyAdmin
from apps.widgets.resource_goal.models import WaterGoalSetting, WaterGoal, WaterBaselineDaily, \
    WaterBaselineHourly


admin.site.register(WaterGoalSetting, GoalSettingsAdmin)
admin.site.register(WaterGoal, GoalAdmin)
admin.site.register(WaterBaselineDaily, BaselineDailyAdmin)

challenge_mgr.register_designer_game_info_model("Water Game", WaterGoalSetting)
challenge_mgr.register_admin_game_info_model("Water Game", WaterUsage)
challenge_mgr.register_admin_challenge_info_model("Status", 1, WaterGoal, 3)
challenge_mgr.register_developer_game_info_model("Water Game", WaterGoalSetting)
challenge_mgr.register_developer_game_info_model("Water Game", WaterGoal)
challenge_mgr.register_developer_game_info_model("Water Game", WaterBaselineDaily)
challenge_mgr.register_developer_game_info_model("Water Game", WaterBaselineHourly)
