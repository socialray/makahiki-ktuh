"""Handle rendering of energy goal widget."""
import datetime

from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.resource_mgr import resource_mgr
from apps.widgets.energy_goal import energy_goal

from apps.widgets.smartgrid import smartgrid


def supply(request, page_name):
    """Supply the view_objects content for this widget."""
    _ = page_name
    user = request.user
    team = user.get_profile().team
    golow_activities = smartgrid.get_available_golow_actions(user)
    goal = None
    daily_goal = None
    is_manual_entry = None
    if team:
        is_manual_entry = energy_goal.is_manual_entry(team)
        if not is_manual_entry:
            goal = get_realtime_goal_data(team)
        daily_goal = get_daily_energy_goal_data(team)

    resource_settings = resource_mgr.get_resource_settings(page_name)

    return {
        "golow_activities": golow_activities,
        "goal": goal,
        "is_manual_entry": is_manual_entry,
        "daily_goal": daily_goal,
        "resource": resource_settings,
        }


def get_realtime_goal_data(team):
    """:return: the energy goal data for the user's team."""
    date = datetime.datetime.today()
    data = resource_mgr.team_energy_data(date=date.date(), team=team)

    if data:
        goal = {}
        goal["goal_usage"] = energy_goal.team_hourly_goal_usage(date=date, team=team)
        goal["warning_usage"] = energy_goal.team_hourly_warning_usage(date, team=team)
        goal["actual_usage"] = data.usage
        goal["updated_at"] = data.updated_at
        goal["actual_diff"] = abs(goal["actual_usage"] - goal["goal_usage"])
        return goal
    else:
        return None


def get_daily_energy_goal_data(team):
    """:return: the daily energy goal data."""

    round_info = challenge_mgr.get_current_round_info()
    start = round_info["start"].date()
    end = round_info["end"].date()
    delta = (end - start).days
    data_table = []
    for day in range(0, delta):
        date = start + datetime.timedelta(days=day)

        goal_info = {}
        goal_info["date"] = date
        goals = team.energygoal_set.filter(date=date)
        if goals:
            goal_info["goal_status"] = goals[0].goal_status
            goal_info["verbose_info"] = "%d kWh used within the last 24 hours (ends at %s). " \
                                        "The goal is %d kWh." % (
                resource_mgr.team_energy_usage(date, team),
                energy_goal.team_goal_settings(team).manual_entry_time,
                energy_goal.team_daily_goal_usage(date, team)
            )

        data_table.append(goal_info)

    return data_table
