"""Energy goal widget administrator interface; shows the team, actual vs. goal, last update."""

from django.contrib import admin


class GoalSettingsAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["team", "goal_percent_reduction", "goal_points", "manual_entry",]


class GoalAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["team", "date", "goal_status"]


class BaselineDailyAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["team", "day", "usage"]


class BaselineHourlyAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["team", "day", "hour", "usage"]
