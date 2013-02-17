"""Energy goal widget administrator interface; shows the team, actual vs. goal, last update."""

from django.contrib import admin
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.resource_mgr.models import EnergyUsage
from apps.widgets.resource_goal.admin import GoalSettingsAdmin, GoalAdmin, BaselineDailyAdmin, \
    BaselineHourlyAdmin
from apps.widgets.resource_goal.models import EnergyGoalSetting, EnergyGoal, EnergyBaselineDaily, \
    EnergyBaselineHourly
from apps.admin.admin import challenge_designer_site, challenge_manager_site, developer_site


admin.site.register(EnergyGoalSetting, GoalSettingsAdmin)
challenge_designer_site.register(EnergyGoalSetting, GoalSettingsAdmin)
challenge_manager_site.register(EnergyGoalSetting, GoalSettingsAdmin)
developer_site.register(EnergyGoalSetting, GoalSettingsAdmin)
admin.site.register(EnergyGoal, GoalAdmin)
challenge_designer_site.register(EnergyGoal, GoalAdmin)
challenge_manager_site.register(EnergyGoal, GoalAdmin)
developer_site.register(EnergyGoal, GoalAdmin)
admin.site.register(EnergyBaselineDaily, BaselineDailyAdmin)
challenge_designer_site.register(EnergyBaselineDaily, BaselineDailyAdmin)
challenge_manager_site.register(EnergyBaselineDaily, BaselineDailyAdmin)
developer_site.register(EnergyBaselineDaily, BaselineDailyAdmin)
admin.site.register(EnergyBaselineHourly, BaselineHourlyAdmin)
challenge_designer_site.register(EnergyBaselineHourly, BaselineHourlyAdmin)
challenge_manager_site.register(EnergyBaselineHourly, BaselineHourlyAdmin)
developer_site.register(EnergyBaselineHourly, BaselineHourlyAdmin)

challenge_mgr.register_designer_game_info_model("Energy Game", EnergyGoalSetting)
challenge_mgr.register_admin_game_info_model("Energy Game", EnergyUsage)
challenge_mgr.register_admin_challenge_info_model("Status", 1, EnergyGoal, 2)
challenge_mgr.register_developer_game_info_model("Energy Game", EnergyGoalSetting)
challenge_mgr.register_developer_game_info_model("Energy Game", EnergyGoal)
challenge_mgr.register_developer_game_info_model("Energy Game", EnergyBaselineDaily)
challenge_mgr.register_developer_game_info_model("Energy Game", EnergyBaselineHourly)
