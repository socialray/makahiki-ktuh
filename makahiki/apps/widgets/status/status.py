"""module for status collection and analysis."""
from apps.managers.player_mgr.models import Profile
from apps.widgets.status.models import DailyStatus
import datetime
from apps.managers.resource_mgr import resource_mgr
from apps.widgets.resource_goal import resource_goal
from apps.widgets.resource_goal.views import get_hourly_goal_data
from apps.utils import utils


def update_daily_status():
    """update the daily user stats."""
    today = datetime.datetime.today()
    date = today.date()

    # if it is run on mid night, we should count previous day's data
    if today.hour == 0:
        date -= datetime.timedelta(days=1)
    count = Profile.objects.filter(last_visit_date=date).count()
    total = Profile.objects.filter(setup_profile=True).count()

    print '*** daily visitors: %d, total: %d at %s\n' % (count, total, today)

    # update the daily total visitor count, and total setup user count
    entry, _ = DailyStatus.objects.get_or_create(short_date=date)
    entry.date = "%s" % date
    entry.daily_visitors = count
    entry.setup_users = total

    entry.save()


def resource_goal_status(resource):
    """supply status data."""

    hist_size = 7

    #establish dates of interest
    today = datetime.datetime.today()
    date_list = _createDateList(hist_size, today)
    resource_goals = _createData(date_list, resource, today)

    return {
        "date_list": date_list,
        "resource_goals": resource_goals,
    }


def _createDateList(hist_size, today):
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
    if hourly_goal and 'actual_usage' in hourly_goal:
        goal_value["actual_usage"] = hourly_goal["actual_usage"]
        goal_value["goal_usage"] = hourly_goal["goal_usage"]
        goal_value["net_usage"] = goal_value["goal_usage"] - goal_value["actual_usage"]
        goal_value["today"] = True
    else:
        goal_value = "N/A"
    return goal_value


def _init_data(team, resource, today):
    """initialize the goal data."""
    data = dict()
    data["name"] = team
    data["vals"] = []
    # also create today's usage
    data["vals"].append((today, _get_today_usage(data["name"], resource)))
    return data


def _createData(date_list, resource, today):
    """Creates the datatable to be used."""
    resource_goals = []

    rate = resource_mgr.get_resource_setting(resource).conversion_rate

    rgoal = resource_goal.get_resource_goal(resource)

    goals = rgoal.objects.filter(
        date__lte=today - datetime.timedelta(days=1),
        date__gte=today - datetime.timedelta(days=(len(date_list) - 1))).order_by(
            'team', '-date').select_related('team')

    data = None
    for goal in goals:
        if data:
            if data["name"] != goal.team:
                # encounter a new team, store the old team data
                resource_goals.append(data)

                # init the new team structure
                data = _init_data(goal.team, resource, today)
        else:
            data = _init_data(goal.team, resource, today)

        goal.goal_usage = utils.format_usage(goal.goal_usage, rate)
        if goal.actual_usage:
            goal.actual_usage = utils.format_usage(goal.actual_usage, rate)
            goal.net_usage = goal.goal_usage - goal.actual_usage
        else:
            goal.net_usage = 'N/A'
        data["vals"].append((goal.date, goal))

    # need to store the last team data
    resource_goals.append(data)

    return resource_goals
