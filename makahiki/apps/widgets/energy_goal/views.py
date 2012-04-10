"""Handle rendering of energy goal widget."""

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from apps.lib.gviz_api import gviz_api
from apps.widgets.energy_goal.models import TeamEnergyGoal

from apps.widgets.smartgrid import get_available_golow_activities


def supply(request, page_name):
    """Supply the view_objects content for this widget."""
    _ = page_name
    user = request.user
    golow_activities = get_available_golow_activities(user)
    goal = TeamEnergyGoal.objects.filter(team=user.get_profile().team).order_by("-updated_at")[0]
    goal.actual_diff = abs(goal.actual_usage - goal.goal_usage)

    return {
        "golow_activities": golow_activities,
        "goal": goal,
        "daily_goal": get_daily_energy_goal_data(request),
        }


@login_required
def energy_goal_data(request):
    """:return: the gviz json format of the energy goal data."""
    user = request.user

    description = {"A": ("string", "Source"),
                   "B": ("date", "Last Update"),
                   "C": ("number", "Actual"),
                   "D": ("number", "Goal"),
                   "E": ("number", "Warning")}

    # Loading it into gviz_api.DataTable
    data_table = gviz_api.DataTable(description)

    goal = TeamEnergyGoal.objects.filter(team=user.get_profile().team).order_by("-updated_at");

    if goal:
        data = [{"A": goal[0].team.name,
                 "B": goal[0].updated_at,
                 "C": goal[0].actual_usage,
                 "D": goal[0].goal_usage,
                 "E": goal[0].warning_usage
                }]
    data_table.AppendData(data)

    return HttpResponse(data_table.ToResponse(tqx="reqId:1"))


@login_required
def get_daily_energy_goal_data(request):
    """:return: the gviz json format of the daily energy goal data."""
    user = request.user

    goal_data = TeamEnergyGoal.objects.filter(team=user.get_profile().team).order_by(
        "updated_at")[:7]
    days = 0
    data_table = []
    for goal in goal_data:
        days = days + 1
        data_table.append(goal)
    days = days + 1
    for day in range(days, 8):
        data_table.append(None)

    return data_table
