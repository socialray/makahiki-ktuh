"""Energy goal widget administrator interface; shows the team, actual vs. goal, last update."""

from django.contrib import admin

from apps.widgets.resource_goal.models import EnergyGoal, WaterGoal, \
    EnergyBaselineDaily, WaterGoalSetting, EnergyGoalSetting, WaterBaselineDaily, \
    EnergyBaselineHourly


class GoalSettingsAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["team", "goal_percent_reduction", "manual_entry_time"]

admin.site.register(EnergyGoalSetting, GoalSettingsAdmin)
admin.site.register(WaterGoalSetting, GoalSettingsAdmin)


class GoalAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["team", "date", "goal_status"]

admin.site.register(EnergyGoal, GoalAdmin)
admin.site.register(WaterGoal, GoalAdmin)


class BaselineDailyAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["day", "team", "usage"]

admin.site.register(EnergyBaselineDaily, BaselineDailyAdmin)
admin.site.register(WaterBaselineDaily, BaselineDailyAdmin)


class BaselineHourlyAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["day", "hour", "team", "usage"]

admin.site.register(EnergyBaselineHourly, BaselineHourlyAdmin)
