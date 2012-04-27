"""Energy goal widget administrator interface; shows the team, actual vs. goal, last update."""

from django.contrib import admin

from apps.widgets.energy_goal.models import EnergyGoal, EnergyGoalSettings


class EnergyGoalSettingsAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["team", "goal_percent_reduction", "manual_entry_time"]

admin.site.register(EnergyGoalSettings, EnergyGoalSettingsAdmin)


class EnergyGoalAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["team", "date", "goal_status"]

admin.site.register(EnergyGoal, EnergyGoalAdmin)
