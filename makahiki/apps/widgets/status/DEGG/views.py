"""Power meters visualization."""

import datetime
from apps.managers.resource_mgr import resource_mgr
from apps.widgets.resource_goal.models import EnergyGoal
from apps.widgets.resource_goal.views import get_hourly_goal_data
from apps.utils import utils


def supply(request, page_name):
    """ Call the remote viz request."""

    _ = page_name
    _ = request

    hist_size = 7
    resource = 'energy'

    #establish dates of interest
    today = datetime.datetime.today()
    date_list = createDateList(hist_size, today)
    energy_goals = createData(date_list, resource, today)

    return {
        "date_list": date_list,
        "energy_goals": energy_goals,
    }


def createDateList(hist_size, today):
    """Sets up dates of interest."""
    datelist = []
    hist_time = (today - datetime.timedelta(days=hist_size - 1))
    while hist_time <= today:
        datelist.append(hist_time)
        hist_time += datetime.timedelta(days=1)
    datelist.reverse()
    return datelist


def _get_today_usage(team, resource):
    """return today's hourly goal usage."""
    goal_value = dict()
    #calculate today's usage
    hourly_goal = get_hourly_goal_data(team, resource)
    if 'actual_usage' in hourly_goal:
        goal_value["actual_usage"] = hourly_goal["actual_usage"]
        goal_value["goal_usage"] = hourly_goal["goal_usage"]
        goal_value["net_usage"] = goal_value["goal_usage"] - goal_value["actual_usage"]
        goal_value["today"] = True
    else:
        goal_value = "N/A"
    return goal_value


def init_data(team, resource, today):
    """initialize the goal data."""
    data = dict()
    data["name"] = team
    data["vals"] = []
    # also create today's usage
    data["vals"].append((today, _get_today_usage(data["name"], resource)))
    return data


def createData(date_list, resource, today):
    """Creates the datatable to be used."""
    energy_goals = []

    rate = resource_mgr.get_resource_setting(resource).conversion_rate
    goals = EnergyGoal.objects.filter(
        date__lte=today - datetime.timedelta(days=1),
        date__gte=today - datetime.timedelta(days=(len(date_list) - 1))).order_by(
            'team', '-date').select_related('team')

    data = None
    for goal in goals:
        if data:
            if data["name"] != goal.team:
                # encounter a new team, store the old team data
                energy_goals.append(data)

                # init the new team structure
                data = init_data(goal.team, resource, today)
        else:
            data = init_data(goal.team, resource, today)

        goal.goal_usage = utils.format_usage(goal.goal_usage, rate)
        goal.actual_usage = utils.format_usage(goal.actual_usage, rate)
        goal.net_usage = goal.goal_usage - goal.actual_usage
        data["vals"].append((goal.date, goal))

    # need to store the last team data
    energy_goals.append(data)

    return energy_goals
