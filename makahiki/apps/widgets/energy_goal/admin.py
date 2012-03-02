"""Admin Definition"""
from django.contrib import admin

from apps.widgets.energy_goal.models import TeamEnergyGoal


class TeamEnergyGoalAdmin(admin.ModelAdmin):
    """EnergyGoal admin"""
    list_display = ["team", "actual_usage", "goal_usage", "warning_usage", "updated_at"]

admin.site.register(TeamEnergyGoal, TeamEnergyGoalAdmin)
