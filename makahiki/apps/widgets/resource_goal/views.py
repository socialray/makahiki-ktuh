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
    user = request.user
    team = user.get_profile().team
    golow_activities = smartgrid.get_available_golow_actions(user, page_name)
    hourly_goal = None
    daily_goal = None
    goal_settings = None
    if team:
        goal_settings = resource_goal.team_goal_settings(team, page_name)
        if not goal_settings.manual_entry and not "calendar_view" in request.GET:
            hourly_goal = get_hourly_goal_data(team, page_name)
        else:
            daily_goal = get_daily_goal_data(team, page_name)

    resource_setting = resource_mgr.get_resource_setting(page_name)

    return {
        "golow_activities": golow_activities,
        "hourly_goal": hourly_goal,
        "daily_goal": daily_goal,
        "resource": resource_setting,
        "goal_settings": goal_settings,
        }


def get_hourly_goal_data(team, resource):
    """:return: the energy goal data for the user's team."""
    date = datetime.datetime.today()
    goal = {"resource": resource}
    if resource_mgr.is_blackout(date):
        return goal.update({"is_blackout": True})

    data = resource_mgr.team_resource_data(date=date.date(), team=team, resource=resource)
    if data:
        goal_settings = resource_goal.team_goal_settings(team, resource)

        baseline = resource_goal.team_hourly_resource_baseline(date, team, resource)

        teamgoal = resource_goal.team_goal(date, team, resource)
        if not teamgoal:
            goal_percentage = goal_settings.goal_percent_reduction
        else:
            goal_percentage = teamgoal.current_goal_percent_reduction

        resource_setting = resource_mgr.get_resource_setting(resource)
        unit = resource_setting.unit
        rate = resource_setting.conversion_rate

        goal.update({"goal_usage": baseline * (100 - goal_percentage) / 100 / rate,
                "warning_usage": baseline * (100 - goal_percentage / 2) / rate,
                "actual_usage": data.usage / rate,
                "updated_at": datetime.datetime.combine(date=data.date, time=data.time),
                "unit": unit,
               })
        goal["actual_diff"] = abs(goal["actual_usage"] - goal["goal_usage"])
        return goal
    else:
        return goal.update({"actual_usage": None})


def get_daily_goal_data(team, resource):
    """:return: the daily energy goal data."""

    round_info = challenge_mgr.get_round_info()
    if not round_info:
        return None

    today = datetime.date.today()
    start = round_info["start"].date()
    end = round_info["end"].date()
    delta = (end - start).days + 1
    data_table = []
    for day in range(0, delta):
        date = start + datetime.timedelta(days=day)
        goal_info = {"date": date, "resource": resource}

        if day == 0:
            # cal and store the filler_days in the first day goal_info
            goal_info["filler_days"] = range(0, date.weekday())

        if day == (delta - 1):
            # cal and store the filler_days in the last day goal_info
            goal_info["filler_days"] = range(0, 6 - date.weekday())

        if date <= today:
            if date == datetime.date.today():
                goal_info["is_today"] = True

            if resource_mgr.is_blackout(date):
                # the game is disabled for the blackout dates
                goal_info["goal_status"] = "Not available"
                goal_info["verbose_info"] = "Game disabled for today"
            else:
                _set_goal_info(goal_info, resource, team, date)

        data_table.append(goal_info)

    return data_table


def _set_goal_info(goal_info, resource, team, date):
    """set the goal info."""
    resource_setting = resource_mgr.get_resource_setting(resource)
    unit = resource_setting.unit
    rate = resource_setting.conversion_rate
    goal_settings = resource_goal.team_goal_settings(team, resource)
    goal = resource_goal.team_goal(date, team, resource)
    goal_percent = resource_goal.get_goal_percent(date, team, resource, goal_settings)
    if goal:
        goal_info["goal_status"] = goal.goal_status
        if goal.actual_usage:
            goal_info["goal_info"] = "usage:<br/>%d %s" % (goal.actual_usage / rate, unit)
        elif goal.goal_usage:
            goal_info["goal_info"] = "goal:%d %s<br/>(reduce %d%%)" % (
                goal.goal_usage / rate, unit, goal_percent)
    else:
        goal_info["goal_status"] = "Unknown"

    if goal_info["goal_status"] == "Not available":
        goal_info["verbose_info"] = "Game disabled for today because baseline data " \
                                    "not available."
    elif goal_info["goal_status"] == "Unknown":
        if date == datetime.date.today():
            # if there is baseline, display the expected goal,
            # otherwise, display disabled with no baseline, as unavailable
            baseline = resource_goal.team_daily_resource_baseline(
                date, team, resource)
            if baseline:
                goal_usage = baseline * (100 - goal_percent) / 100
                goal_info["goal_status"] = None
                goal_info["goal_info"] = "goal:%d %s<br/>(reduce %d%%)" % (
                    goal_usage / rate, unit, goal_percent)
            else:
                goal_info["goal_status"] = "Not available"
                goal_info["verbose_info"] = "Game disabled for today because " \
                                            "baseline data not available."
        else:
            goal_info["goal_status"] = "Not available"
            goal_info["verbose_info"] = "Game disabled for today because usage data " \
                                    "not available."
    else:
        goal_info["verbose_info"] = "%d %s used within the last 24 hours (ends at %s). " \
        "<br/>The goal is %d %s (reduce %d%%)." % (
                goal.actual_usage / rate,
                unit,
                goal_settings.manual_entry_time if goal_settings.manual_entry else "midnight",
                goal.goal_usage / rate,
                unit,
                goal_percent
            )
