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

    return {
        "golow_activities": golow_activities,
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

    try:
        goal = TeamEnergyGoal.objects.get(team=user.get_profile().team)
        data = [{"A": goal.team.name,
                 "B": goal.updated_at,
                 "C": goal.actual_usage,
                 "D": goal.goal_usage,
                 "E": goal.warning_usage
                }]
        data_table.AppendData(data)
    except ObjectDoesNotExist:
        pass

    return HttpResponse(data_table.ToResponse(tqx="reqId:1"))
