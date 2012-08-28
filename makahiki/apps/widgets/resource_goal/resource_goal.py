"""Implements the Daily Energy (or Water) Goal Game."""

import datetime
from django.db.models.aggregates import Count, Avg
from django.template.defaultfilters import slugify
import requests
from apps.managers.cache_mgr import cache_mgr
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.resource_mgr import resource_mgr
from apps.managers.team_mgr.models import Team
from apps.widgets.resource_goal.models import EnergyGoal, WaterGoal, WaterGoalSetting, \
    EnergyGoalSetting, EnergyBaselineDaily, WaterBaselineDaily, EnergyBaselineHourly, \
    WaterBaselineHourly


def team_goal_settings(team, resource):
    """Returns the goal settings for the given team and resource."""
    if resource == "energy":
        goalsetting = EnergyGoalSetting
    elif resource == "water":
        goalsetting = WaterGoalSetting

    goalsettings = goalsetting.objects.filter(team=team)
    if goalsettings:
        return goalsettings[0]
    else:
        return None


def is_manual_entry(team, resource):
    """Returns true if the game uses manual entry for the given team and resource."""
    gs = team_goal_settings(team, resource)
    return gs.manual_entry if gs else None


def _get_resource_goal(resource):
    """Return the resource goal object."""
    if resource == "energy":
        return EnergyGoal
    elif resource == "water":
        return WaterGoal
    else:
        return None


def team_goal(date, team, resource):
    """Returns the team's goal status for the given resource."""
    goal = _get_resource_goal(resource)
    goals = goal.objects.filter(date=date, team=team)
    if goals:
        return goals[0]
    else:
        return None


def team_daily_goal_usage(date, team, resource, goal_settings):
    """Returns the goal usage of the current date and resource."""
    goal_percent = goal_settings.goal_percent_reduction
    baseline_usage = 0
    baseline_usage = team_daily_resource_baseline(date, team, resource)
    if goal_settings.baseline_method == "Dynamic":
        # get previous day's goal result and the current goal percent
        previous_goal_result = team_goal(date - datetime.timedelta(days=1), team, resource)
        if previous_goal_result and previous_goal_result.current_goal_percent_reduction:
            goal_percent = previous_goal_result.current_goal_percent_reduction

    usage = (baseline_usage * 100 - baseline_usage * goal_percent) / 100
    return usage


def _get_baseline_date(date):
    """Returns a non-blackout date that is one weeks prior."""
    baseline_date = date - datetime.timedelta(days=7)
    if resource_mgr.is_blackout(baseline_date):
        return _get_baseline_date(baseline_date)
    else:
        return baseline_date


def team_daily_resource_baseline(date, team, resource):
    """Returns the baseline usage for the date and resource."""
    if resource == "energy":
        daily_baseline = EnergyBaselineDaily
    elif resource == "water":
        daily_baseline = WaterBaselineDaily
    else:
        return None

    day = date.weekday()
    baselines = daily_baseline.objects.filter(team=team, day=day)
    if baselines:
        return baselines[0].usage
    else:
        return 0


def team_hourly_resource_baseline(date, team, resource):
    """Returns the baseline usage for the date and resource."""
    if resource == "energy":
        hourly_baseline = EnergyBaselineHourly
    elif resource == "water":
        hourly_baseline = WaterBaselineHourly
    else:
        return None

    day = date.weekday()
    hour = date.time().hour
    baselines = hourly_baseline.objects.filter(team=team, day=day, hour=hour)
    if baselines:
        return baselines[0].usage
    else:
        return 0


def update_energy_baseline(end_date, weeks, method):
    """calculate the energy baseline from the specified end_date and week period."""
    session = requests.session()

    for team in Team.objects.all():
        goal_settings = team_goal_settings(team, "energy")
        if goal_settings.baseline_method == method:
            cal_energy_baseline(session, team, method, end_date, weeks)


def cal_energy_baseline(session, team, method, end_date, weeks):
    """calculate the fixed energy baseline from the specified end_date and week period."""

    # energy daily
    if method == "Fixed":
        day_range = 7
    else:
        day_range = 1

    date = end_date
    for day in range(0, day_range):
        date -= datetime.timedelta(days=day)
        usage = get_energy_baseline_usage(session, team, date, weeks, None)
        baseline, _ = EnergyBaselineDaily.objects.get_or_create(team=team, day=date.weekday())
        baseline.usage = usage
        baseline.save()

    # energy hourly
    date = end_date
    for day in range(0, day_range):
        date -= datetime.timedelta(days=day)
        for hour in range(1, 25):
            usage = get_energy_baseline_usage(session, team, date, weeks, hour)
            baseline, _ = EnergyBaselineHourly.objects.get_or_create(team=team,
                                                                     day=date.weekday(),
                                                                     hour=hour)
            baseline.usage = usage
            baseline.save()

    print 'team %s energy baseline usage updated.' % team


def get_energy_baseline_usage(session, team, end_date, weeks, hour):
    """Returns the daily or hourly energy baseline usage from the history data."""
    usage = 0
    count = 0
    date = end_date
    for week in range(0, weeks):
        _ = week
        date = _get_baseline_date(date)
        start_time = date.strftime("%Y-%m-%dT00:00:00")
        if hour:
            end_time = date.strftime("%Y-%m-%dT") + "%.2d:00:00" % hour
        else:
            end_time = (date + datetime.timedelta(days=1)).strftime("%Y-%m-%dT00:00:00")

        session.params = {'startTime': start_time, 'endTime': end_time}
        usage += resource_mgr.get_energy_usage(session, team.name)
        if usage:
            count += 1
    return usage / count


def _adjust_goal_percent(date, team, resource, goal_settings, goal):
    """adjust the dynamimc goal percent. it is called only when the current day's goal is met.
     the current goal percent is 1 percent less from the previous day's goal percent unless the
     previous goal percent is already 1."""
    previous_goal_result = team_goal(date - datetime.timedelta(days=1), team, resource)
    if previous_goal_result:
        if previous_goal_result.current_goal_percent_reduction > 1:
            goal.current_goal_percent_reduction -= 1
    else:
        goal.current_goal_percent_reduction = goal_settings.goal_percent_reduction - 1


def check_daily_resource_goal(team, resource):
    """Check the daily goal, award points to the team members if the goal is met.
    Returns the number of players in the team that got the award."""

    # because the check is scheduled at midnight, we should check the previous day's data
    today = datetime.datetime.today()
    if today.hour == 0:
        today = today - datetime.timedelta(hours=1)
    # do nothing if out of round
    rounds_info = challenge_mgr.get_all_round_info()
    if not rounds_info["competition_start"] < today < rounds_info["competition_end"]:
        return 0

    date = today.date()
    actual_usage = None

    resource_data = resource_mgr.team_resource_data(date, team, resource)
    if resource_data:
        goal_settings = team_goal_settings(team, resource)
        goal_usage = team_daily_goal_usage(date, team, resource, goal_settings)

        # check if the manual entry time is within the target time,
        # otherwise can not determine the actual usage
        if not goal_settings.manual_entry or  \
            (goal_settings.manual_entry_time.hour <= resource_data.time.hour and\
             resource_data.time.hour <= (goal_settings.manual_entry_time.hour + 1)):
            actual_usage = resource_data.usage

    count = 0

    goal = _get_resource_goal(resource)
    goal, _ = goal.objects.get_or_create(team=team, date=date)

    if actual_usage:
        if actual_usage <= goal_usage:
            # if already awarded, do nothing
            if goal.goal_status != "Below the goal":
                goal.goal_status = "Below the goal"

                # record the reduction percentage
                goal.percent_reduction = (goal_usage - actual_usage) * 100 / goal_usage

                # adjust the current goal percentage
                _adjust_goal_percent(date, team, resource, goal_settings, goal)

                # Award points to the members of the team.
                goal_points = goal_settings.goal_points
                for profile in team.profile_set.all():
                    if profile.setup_complete:
                        today = datetime.datetime.today()
                        # Hack to get around executing this script at midnight.  We want to award
                        # points earlier to ensure they are within the round they were completed.
                        if today.hour == 0:
                            today = today - datetime.timedelta(hours=1)

                        date = "%d/%d/%d" % (today.month, today.day, today.year)
                        profile.add_points(goal_points, today,
                                           "Team %s Goal for %s" % (resource, date), goal)
                        profile.save()
                        count += 1
        else:
            goal.goal_status = "Over the goal"
    else:
        # if can not determine the actual usage, set the status to unknown
        goal.goal_status = "Unknown"

    goal.save()

    return count


def check_all_daily_resource_goals(resource):
    """Check the daily resource goal for all teams."""
    is_awarded = False
    for team in Team.objects.all():
        count = check_daily_resource_goal(team, resource)
        if count:
            print '%s users in %s are awarded %s points each.' % (
                count,
                team,
                team_goal_settings(team, resource).goal_points)
            is_awarded = True

    if not is_awarded:
        print 'No user are awarded daily goal points.'


def resource_goal_ranks(resource, round_name=None):
    """Generate the scoreboard for resource goals."""
    cache_key = "%s_goal_ranks-%s" % (resource, slugify(round_name))
    goal_ranks = cache_mgr.get_cache(cache_key)
    if goal_ranks is None:
        goal_ranks = []
        goal = _get_resource_goal(resource)

        round_info = challenge_mgr.get_round_info(round_name)
        if not round_info:
            return None

        ranks = goal.objects.filter(
            goal_status="Below the goal",
            date__lte=round_info["end"].date).values("team__name").annotate(
                completions=Count("team"),
                average_reduction=Avg("percent_reduction")).order_by(
                    "-completions", "-average_reduction")

        for rank in ranks:
            goal_ranks.append(rank)

        total_count = Team.objects.count()
        if len(goal_ranks) != total_count:
            for t in Team.objects.all():
                if not t.name in goal_ranks:
                    rank = {"team__name": t.name,
                            "completions": 0,
                            "average_reduction": 0}
                    goal_ranks.append(rank)
                    if len(goal_ranks) == total_count:
                        break
        cache_mgr.set_cache(cache_key, goal_ranks, 3600 * 24)
    return goal_ranks


def resource_goal_leader(name, round_name=None):
    """Returns the leader (team name) of the resource use."""
    ranks = resource_goal_ranks(name, round_name)
    if ranks:
        return ranks[0]["team__name"]
    else:
        return None
