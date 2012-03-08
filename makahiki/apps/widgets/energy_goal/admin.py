"""Energy goal widget administrator interface; shows the team, actual vs. goal, last update."""

from django.contrib import admin

from apps.widgets.energy_goal.models import TeamEnergyGoal


class TeamEnergyGoalAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["team", "actual_usage", "goal_usage", "warning_usage", "updated_at"]

admin.site.register(TeamEnergyGoal, TeamEnergyGoalAdmin)
