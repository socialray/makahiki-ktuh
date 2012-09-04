"""Power meters visualization."""

import datetime
from apps.widgets.resource_goal.models import EnergyGoal
from apps.widgets.resource_goal.resource_goal import team_goal_settings, get_goal_percent
from apps.widgets.resource_goal.resource_goal import team_daily_resource_baseline
from apps.widgets.resource_goal.views import get_hourly_goal_data
from apps.managers.team_mgr.models import Team


def supply(request, page_name):
    """ Call the remote viz request."""

    _ = page_name
    _ = request

    hist_size = 7
    resource = 'energy'
    #establish dates of interest
    datelist = createDateList(hist_size)

    #create the table
    teams = Team.objects.all()
    table = createDataTable(teams, datelist, resource)

    return {
        "energy_goals": table["energy_goals"],
        "date_list": table["date_list"],
    }


def createDateList(hist_size):
    """Sets up dates of interest."""
    datelist = []
    today = datetime.datetime.today()
    hist_time = (today - datetime.timedelta(days=hist_size))
    while hist_time < today:
        datelist.append(hist_time)
        hist_time += datetime.timedelta(days=1)
    datelist.reverse()
    return datelist


def createDataTable(teams, datelist, resource):
    """Creates the datatable to be used."""

    today = datetime.datetime.today()
    energy_goals = []
    for team in teams:
        vals = []

        #calculate today's baseline
        goal_percent = get_goal_percent(today, team, resource, team_goal_settings(team, resource))
        goal_value = dict()
        goal_value["goal_usage"] = (100 - goal_percent) * team_daily_resource_baseline(today,
        team, resource) / 100

        #calculate today's usage
        hourly_goal = get_hourly_goal_data(team, resource)
        goal_value["actual_usage"] = hourly_goal["actual_usage"]
        goal_value["net_usage"] = goal_value["goal_usage"] - goal_value["actual_usage"]
        vals.append((today, goal_value))

        goals = EnergyGoal.objects.filter(team_id=team.id).order_by('-date')
        data = dict()
        data["name"] = team.name

        for date in datelist:
            entries = goals.filter(date=date)
            if entries.count() < 1:
                entries = "N/A"
            else:
                #strip off the queryset wrapper
                entries = entries[0]
                #calculate net usage
                entries.net_usage = entries.goal_usage - entries.actual_usage
            vals.append((date, entries))

        data["vals"] = vals
        energy_goals.append(data)
    return {
        "energy_goals": energy_goals,
        "date_list": datelist,
    }
