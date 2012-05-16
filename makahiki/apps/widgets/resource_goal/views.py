"""Handle rendering of energy goal widget."""
import datetime

from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.resource_mgr import resource_mgr
from apps.widgets.resource_goal import resource_goal

from apps.widgets.smartgrid import smartgrid


def supply(request, page_name):
    """base view supply is not used. The child widget view supply should call resource_supply."""
    _ = request
    _ = page_name
    return {}


def resource_supply(request, page_name):
    """Supply the view_objects content for this widget."""
    _ = page_name
    user = request.user
    team = user.get_profile().team
    golow_activities = smartgrid.get_available_golow_actions(user, page_name)
    hourly_goal = None
    daily_goal = None
    if team:
        if not resource_goal.is_manual_entry(team, page_name):
            hourly_goal = get_hourly_goal_data(team, page_name)
        else:
            daily_goal = get_daily_goal_data(team, page_name)

    resource_settings = resource_mgr.get_resource_settings(page_name)

    return {
        "golow_activities": golow_activities,
        "hourly_goal": hourly_goal,
        "daily_goal": daily_goal,
        "resource": resource_settings,
        }


def get_hourly_goal_data(team, resource):
    """:return: the energy goal data for the user's team."""
    date = datetime.datetime.today()
    data = resource_mgr.team_resource_data(date=date.date(), team=team, resource=resource)

    if data:
        goal_settings = resource_goal.team_goal_settings(team, resource)
        goal_percentage = goal_settings.goal_percent_reduction
        warning_percentage = goal_settings.warning_percent_reduction
        baseline = resource_goal.team_hourly_resource_baseline(date, team, resource)
        goal = {"goal_usage": (baseline * 100 - baseline * goal_percentage) / 100 / 1000,
                "warning_usage": (baseline * 100 - baseline * warning_percentage) / 100 / 100,
                "actual_usage": data.usage,
                "updated_at": data.updated_at}
        goal["actual_diff"] = abs(goal["actual_usage"] - goal["goal_usage"])
        return goal
    else:
        return None


def get_daily_goal_data(team, resource):
    """:return: the daily energy goal data."""

    round_info = challenge_mgr.get_current_round_info()
    if not round_info:
        return None

    start = round_info["start"].date()
    end = round_info["end"].date()
    delta = (end - start).days
    data_table = []
    for day in range(0, delta):
        date = start + datetime.timedelta(days=day)

        goal_info = {"date": date}
        goal = resource_goal.team_goal(date, team, resource)
        if goal:
            unit = resource_mgr.get_resource_settings(resource).unit
            goal_info["goal_status"] = goal.goal_status
            goal_info["verbose_info"] = "%d %s used within the last 24 hours (ends at %s). " \
                                        "The goal is %d %s." % (
                resource_mgr.team_resource_usage(date, team, resource) / 1000,
                unit,
                resource_goal.team_goal_settings(team, resource).manual_entry_time,
                resource_goal.team_daily_goal_usage(date, team, resource) / 1000,
                unit
            )

        data_table.append(goal_info)

    return data_table
