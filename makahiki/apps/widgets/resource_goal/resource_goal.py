"""daily energy_goal game module."""

import datetime
from django.db.models.aggregates import Count
from apps.managers.resource_mgr import resource_mgr
from apps.widgets.resource_goal.models import EnergyGoal, WaterGoal, WaterGoalSetting, \
    EnergyGoalSetting, EnergyBaselineDaily, WaterBaselineDaily, EnergyBaselineHourly, \
    WaterBaselineHourly


def team_goal_settings(team, resource):
    """returns the energy goal settings for the team."""
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
    """returns true if the team's data is manual entry."""
    return team_goal_settings(team, resource).manual_entry


def _get_resource_goal(resource):
    """return the resource goal object."""
    if resource == "energy":
        return EnergyGoal
    elif resource == "water":
        return WaterGoal
    else:
        return None


def team_goal(date, team, resource):
    """returns the team's goal status."""

    goal = _get_resource_goal(resource)
    goals = goal.objects.filter(date=date, team=team)
    if goals:
        return goals[0]
    else:
        return None


def team_daily_goal_usage(date, team, resource):
    """Returns the goal usage of the current date."""
    goal_percentage = team_goal_settings(team, resource).goal_percent_reduction

    baseline_usage = team_daily_resource_baseline(date, team, resource)

    usage = (baseline_usage * 100 - baseline_usage * goal_percentage) / 100
    return usage


def team_daily_resource_baseline(date, team, resource):
    """Returns the energy baseline usage for the date."""

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
    """Returns the energy baseline usage for the date."""

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


def check_daily_resource_goal(team, resource):
    """check the daily energy goal, award points to the team members if the goal is meet.
    Returns the number of players in the team got the award."""

    date = datetime.date.today()
    goal_settings = team_goal_settings(team, resource)
    goal_usage = team_daily_goal_usage(date, team, resource)
    resource_data = resource_mgr.team_resource_data(date, team, resource)
    actual_usage = None
    if resource_data:
        # check if the manual entry time is within the target time,
        # otherwise can not determine the actual usage
        if not goal_settings.manual_entry or  \
            (goal_settings.manual_entry_time.hour <= resource_data.time.hour and\
             resource_data.time.hour <= (goal_settings.manual_entry_time.hour + 1)):
            actual_usage = resource_data.usage

    count = 0

    goal = _get_resource_goal(resource)
    goal, _ = goal.objects.get_or_create(team=team, date=date)

    if goal and actual_usage:
        if actual_usage <= goal_usage:
            # if already awarded, do nothing
            if goal.goal_status != "Below the goal":
                goal.goal_status = "Below the goal"
                goal_points = goal_settings.goal_points

                # Award points to the members of the team.
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


def check_daily_energy_goal(team):
    """check the daily energy goal, award points to the team members if the goal is meet.
    Returns the number of players in the team got the award."""
    return check_daily_resource_goal(team, "energy")


def check_daily_water_goal(team):
    """check the daily energy goal, award points to the team members if the goal is meet.
    Returns the number of players in the team got the award."""
    return check_daily_resource_goal(team, "energy")


def energy_goal_ranks():
    """Generate the scoreboard for energy goals."""
    # We could aggregate the energy goals in teams, but there's a bug in Django.
    # See https://code.djangoproject.com/ticket/13461
    return EnergyGoal.objects.filter(
        goal_status="Below the goal"
    ).values(
        "team__name"
    ).annotate(completions=Count("team")).order_by("-completions")
