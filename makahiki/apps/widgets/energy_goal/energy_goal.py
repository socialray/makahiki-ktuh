"""daily energy_goal game module."""

import datetime
from django.core.exceptions import ObjectDoesNotExist
from apps.managers.resource_mgr import resource_mgr
from apps.widgets.energy_goal.models import EnergyGoal


def is_manual_entry(team):
    """return true if the team's data is manual entry."""
    goal_settings = team.energygoalsettings_set.all()[0]
    return goal_settings.manual_entry


def current_goal_usage(team):
    """Retun the goal usage of the current date."""
    date = datetime.date.today()
    goal_settings = team.energygoalsettings_set.all()[0]
    goal_percentage = goal_settings.goal_percent_reduction

    try:
        baseline_usage = team.energygoalbaseline_set.get(date=date).baseline_usage
    except ObjectDoesNotExist:
        baseline_usage = 0

    goal_usage = (baseline_usage * 100 - baseline_usage * goal_percentage) / 100
    return goal_usage


def current_warning_usage(team):
    """return the current warning usage."""
    date = datetime.date.today()
    goal_settings = team.energygoalsettings_set.all()[0]
    warning_percentage = goal_settings.warning_percent_reduction

    try:
        baseline_usage = team.energygoalbaseline_set.get(date=date).baseline_usage
    except ObjectDoesNotExist:
        baseline_usage = 0

    warning_usage = (baseline_usage * 100 - baseline_usage * warning_percentage) / 100
    return warning_usage


def check_daily_energy_goal(team):
    """check the dail energy goal, award points to the team members if the goal is meet."""

    date = datetime.date.today()
    goal_usage = current_goal_usage(team)
    energy_data = resource_mgr.team_current_energy_data(team)
    actual_usage = None
    if energy_data:
        # check if the manual entry time is within the target time,
        # otherwise can not determine the actual usage
        goal_settings = team.energygoalsettings_set.all()[0]
        if goal_settings.manual_entry and \
            goal_settings.manual_entry_time.hour <= energy_data.time.hour and\
           energy_data.time.hour <= (goal_settings.manual_entry_time.hour + 1):
            actual_usage = energy_data.usage

    count = 0

    goal = EnergyGoal(team=team, date=date)

    if actual_usage:
        if actual_usage <= goal_usage:

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
