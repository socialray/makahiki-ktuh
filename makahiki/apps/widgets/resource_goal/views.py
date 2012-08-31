"""Handle rendering of energy goal widget."""
import datetime

from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.resource_mgr import resource_mgr
from apps.widgets.resource_goal import resource_goal
from apps.widgets.smartgrid import smartgrid


def supply(request, page_name):
    """Base view supply is not used. The child widget view supply should call resource_supply."""
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

    resource_setting = resource_mgr.get_resource_setting(page_name)

    return {
        "golow_activities": golow_activities,
        "hourly_goal": hourly_goal,
        "daily_goal": daily_goal,
        "resource": resource_setting,
        }


def get_hourly_goal_data(team, resource):
    """:return: the energy goal data for the user's team."""
    date = datetime.datetime.today()
    if resource_mgr.is_blackout(date):
        return {"is_blackout": True}

    data = resource_mgr.team_resource_data(date=date.date(), team=team, resource=resource)
    if data:
        goal_settings = resource_goal.team_goal_settings(team, resource)
        goal_percentage = goal_settings.goal_percent_reduction
        baseline = resource_goal.team_hourly_resource_baseline(date, team, resource)
        if goal_settings.baseline_method == "Dynamic":
            # get previous day's goal result and the current goal percent
            previous_goal_result = resource_goal.team_goal(date - datetime.timedelta(days=1),
                                                           team, resource)
            if previous_goal_result and previous_goal_result.current_goal_percent_reduction:
                goal_percentage = previous_goal_result.current_goal_percent_reduction

        goal = {"goal_usage": baseline * (100 - goal_percentage) / 100 / 100 / 10.0,
                "warning_usage": baseline * (100 - goal_percentage / 2) / 100 / 100 / 10.0,
                "actual_usage": data.usage / 100 / 10.0,
                "updated_at": datetime.datetime.combine(date=data.date, time=data.time)
               }
        goal["actual_diff"] = abs(goal["actual_usage"] - goal["goal_usage"])
        return goal
    else:
        return {"actual_usage": None}


def get_daily_goal_data(team, resource):
    """:return: the daily energy goal data."""

    round_info = challenge_mgr.get_round_info()
    if not round_info:
        return None

    start = round_info["start"].date()
    end = round_info["end"].date()
    delta = (end - start).days + 1
    data_table = []
    for day in range(0, delta):
        date = start + datetime.timedelta(days=day)

        goal_info = {"date": date}

        if day == 0:
            # cal and store the filler_days in the first day goal_info
            goal_info["filler_days"] = range(0, date.weekday())

        if day == (delta - 1):
            # cal and store the filler_days in the last day goal_info
            goal_info["filler_days"] = range(0, 6 - date.weekday())

        goal = resource_goal.team_goal(date, team, resource)
        goal_settings = resource_goal.team_goal_settings(team, resource)
        unit = resource_mgr.get_resource_setting(resource).unit
        goal_usage = resource_goal.team_daily_goal_usage(date, team, resource, goal_settings)
        goal_info["goal_info"] = "%d %s" % (goal_usage, unit)
        if goal:
            goal_info["goal_status"] = goal.goal_status
            goal_info["verbose_info"] = "%d %s used within the last 24 hours (ends at %s). " \
                                        "The goal is %d %s." % (
                resource_mgr.team_resource_usage(date, team, resource),
                unit,
                goal_settings.manual_entry_time,
                goal_usage,
                unit
            )

        data_table.append(goal_info)

    return data_table
