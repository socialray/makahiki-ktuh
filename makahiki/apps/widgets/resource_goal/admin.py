"""Energy goal widget administrator interface; shows the team, actual vs. goal, last update."""

from django.contrib import admin


class GoalSettingsAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["team", "goal_percent_reduction", "manual_entry_time"]


class GoalAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["team", "date", "goal_status"]


class BaselineDailyAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["day", "team", "usage"]


class BaselineHourlyAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["day", "hour", "team", "usage"]
