"""daily energy_goal game module."""

import datetime
from apps.managers.resource_mgr import resource_mgr
from apps.widgets.energy_goal.models import EnergyGoal


def team_goal_settings(team):
    """returns the energy goal settings for the team."""
    return team.energygoalsettings_set.all()[0]


def is_manual_entry(team):
    """returns true if the team's data is manual entry."""
    return team_goal_settings(team).manual_entry


def team_daily_goal_usage(date, team):
    """Returns the goal usage of the current date."""
    goal_percentage = team_goal_settings(team).goal_percent_reduction

    baseline_usage = resource_mgr.team_daily_energy_baseline(date, team)

    usage = (baseline_usage * 100 - baseline_usage * goal_percentage) / 100
    return usage


def team_hourly_goal_usage(date, team):
    """Returns the goal usage of the current date."""
    goal_percentage = team_goal_settings(team).goal_percent_reduction

    baseline_usage = resource_mgr.team_hourly_energy_baseline(date, team)

    usage = (baseline_usage * 100 - baseline_usage * goal_percentage) / 100
    return usage


def team_hourly_warning_usage(date, team):
    """returns the current warning usage."""
    warning_percentage = team_goal_settings(team).warning_percent_reduction

    baseline_usage = resource_mgr.team_hourly_energy_baseline(date, team)

    usage = (baseline_usage * 100 - baseline_usage * warning_percentage) / 100
    return usage


def check_daily_energy_goal(team):
    """check the daily energy goal, award points to the team members if the goal is meet.
    Returns the number of players in the team got the award."""

    date = datetime.date.today()
    goal_usage = team_daily_goal_usage(date, team)
    energy_data = resource_mgr.team_energy_data(date, team)
    actual_usage = None
    if energy_data:
        # check if the manual entry time is within the target time,
        # otherwise can not determine the actual usage
        goal_settings = team_goal_settings(team)
        if not goal_settings.manual_entry or  \
            (goal_settings.manual_entry_time.hour <= energy_data.time.hour and\
             energy_data.time.hour <= (goal_settings.manual_entry_time.hour + 1)):
            actual_usage = energy_data.usage

    count = 0

    goal, _ = EnergyGoal.objects.get_or_create(team=team, date=date)

    if actual_usage:
        if actual_usage <= goal_usage:
            # if already awarded, do nothing
            if goal.goal_status != "Below the goal":
                goal.goal_status = "Below the goal"
                goal_points = team.energygoalsettings_set.all()[0].goal_points

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
                                           "Team Energy Goal for %s" % date, goal)
                        profile.save()
                        count = count + 1
        else:
            goal.goal_status = "Over the goal"
    else:
        # if can not determine the actual usage, set the status to unknown
        goal.goal_status = "Unknown"

    goal.save()

    return count
