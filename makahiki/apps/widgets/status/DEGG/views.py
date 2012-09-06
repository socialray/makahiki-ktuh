"""Power meters visualization."""

import datetime
from django.shortcuts import get_object_or_404
from apps.widgets.resource_goal.models import EnergyGoal
from apps.widgets.resource_goal.resource_goal import team_goal_settings, get_goal_percent
from apps.widgets.resource_goal.resource_goal import team_daily_resource_baseline
from apps.widgets.resource_goal.views import get_hourly_goal_data
from apps.managers.resource_mgr.models import ResourceSetting
from apps.managers.team_mgr.models import Team
from apps.utils import utils


def supply(request, page_name):
    """ Call the remote viz request."""

    _ = page_name
    _ = request

    hist_size = 7
    resource = 'energy'
    teams = Team.objects.all()

    #establish dates of interest
    today = datetime.datetime.today()
    date_list = createDateList(hist_size, today)
    energy_goals = createData(teams, date_list, resource, today)

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


def createData(teams, date_list, resource, today):
    """Creates the datatable to be used."""
    energy_goals = []
    for team in teams:
        vals = []

        #calculate today's baseline
        goal_percent = get_goal_percent(today, team, resource, team_goal_settings(team, resource))
        goal_value = dict()
        goal_value["goal_usage"] = (100 - goal_percent) * team_daily_resource_baseline(today,
        team, resource) / 100
        rate = get_object_or_404(ResourceSetting, name=resource)
        rate = rate.conversion_rate
        goal_value["goal_usage"] = utils.format_usage(goal_value["goal_usage"], rate)

        #calculate today's usage
        hourly_goal = get_hourly_goal_data(team, resource)
        if 'actual_usage' in hourly_goal:
            goal_value["actual_usage"] = hourly_goal["actual_usage"]
            goal_value["hourly_goal"] = hourly_goal["goal_usage"]
            goal_value["net_usage"] = goal_value["goal_usage"] - goal_value["actual_usage"]
            goal_value["today"] = True
        else:
            goal_value = "N/A"
        vals.append((today, goal_value))

        goals = EnergyGoal.objects.filter(team_id=team.id).order_by('-date')
        data = dict()
        data["name"] = team.name

        for date in date_list:
            #We already did today's value
            if date != today:
                entries = goals.filter(date=date)
                if entries.count() < 1:
                    entries = "N/A"
                else:
                    #strip off the queryset wrapper
                    entries = entries[0]
                    #calculate net usage
                    entries.net_usage = (entries.goal_usage - entries.actual_usage) / rate
                    entries.goal_usage = entries.goal_usage / rate
                vals.append((date, entries))

        data["vals"] = vals
        energy_goals.append(data)
    return energy_goals
