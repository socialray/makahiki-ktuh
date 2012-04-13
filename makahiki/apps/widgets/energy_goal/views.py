"""Handle rendering of energy goal widget."""
import datetime

from django.core.exceptions import ObjectDoesNotExist
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.resource_mgr import resource_mgr
from apps.widgets.energy_goal import energy_goal
from apps.widgets.energy_goal.models import EnergyGoal

from apps.widgets.smartgrid import get_available_golow_activities


def supply(request, page_name):
    """Supply the view_objects content for this widget."""
    _ = page_name
    user = request.user
    team = user.get_profile().team
    golow_activities = get_available_golow_activities(user)
    goal = None
    daily_goal = None
    is_manual_entry = None
    if team:
        is_manual_entry = energy_goal.is_manual_entry(team)
        if not is_manual_entry:
            goal = get_realtime_goal_data(team)
        daily_goal = get_daily_energy_goal_data(team)

    return {
        "golow_activities": golow_activities,
        "goal": goal,
        "is_manual_entry": is_manual_entry,
        "daily_goal": daily_goal,
        }


def get_realtime_goal_data(team):
    """:return: the energy goal data for the user's team."""
    data = resource_mgr.team_current_energy_data(team=team)

    if data:
        goal = {}
        goal["goal_usage"] = energy_goal.current_goal_usage(team=team)
        goal["warning_usage"] = energy_goal.current_warning_usage(team=team)
        goal["actual_usage"] = data.usage
        goal["updated_at"] = data.updated_at
        goal["actual_diff"] = abs(goal["actual_usage"] - goal["goal_usage"])
        return goal
    else:
        return None


def get_daily_energy_goal_data(team):
    """:return: the gviz json format of the daily energy goal data."""

    round_info = challenge_mgr.get_current_round_info()
    start = round_info["start"].date()
    end = round_info["end"].date()
    delta = (end - start).days
    data_table = []
    for day in range(0, delta):
        date = start + datetime.timedelta(days=day)
        try:
            goal = EnergyGoal.objects.get(date=date, team=team)
        except ObjectDoesNotExist:
            goal = EnergyGoal(team=team, date=date)

        data_table.append(goal)

    return data_table
