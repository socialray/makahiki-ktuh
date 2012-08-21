"""Energy goal widget administrator interface; shows the team, actual vs. goal, last update."""

from django.contrib import admin
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.resource_mgr.models import WaterUsage
from apps.widgets.resource_goal.admin import GoalSettingsAdmin, GoalAdmin
from apps.widgets.resource_goal.models import WaterGoalSetting, WaterGoal


admin.site.register(WaterGoalSetting, GoalSettingsAdmin)
admin.site.register(WaterGoal, GoalAdmin)

challenge_mgr.register_game_admin_model("resource_goal.water", WaterGoalSetting)
challenge_mgr.register_game_admin_model("resource_goal.water", WaterUsage)
challenge_mgr.register_game_admin_model("resource_goal.water", WaterGoal)
