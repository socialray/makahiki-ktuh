"""Energy goal widget administrator interface; shows the team, actual vs. goal, last update."""

from django.contrib import admin
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.resource_mgr.models import EnergyUsage
from apps.widgets.resource_goal.admin import GoalSettingsAdmin, GoalAdmin, BaselineDailyAdmin, \
    BaselineHourlyAdmin
from apps.widgets.resource_goal.models import EnergyGoalSetting, EnergyGoal, EnergyBaselineDaily, \
    EnergyBaselineHourly


admin.site.register(EnergyGoalSetting, GoalSettingsAdmin)
admin.site.register(EnergyGoal, GoalAdmin)
admin.site.register(EnergyBaselineDaily, BaselineDailyAdmin)
admin.site.register(EnergyBaselineHourly, BaselineHourlyAdmin)

challenge_mgr.register_game_admin_model("resource_goal.energy", EnergyGoalSetting)
challenge_mgr.register_game_admin_model("resource_goal.energy", EnergyUsage)
challenge_mgr.register_sys_admin_model("Resource Goals", EnergyGoal)
challenge_mgr.register_sys_admin_model("Resource Goals", EnergyBaselineDaily)
challenge_mgr.register_sys_admin_model("Resource Goals", EnergyBaselineHourly)
