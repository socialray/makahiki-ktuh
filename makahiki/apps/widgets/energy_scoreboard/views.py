"""Handle the rendering of the energy scoreboard widget."""

import datetime
from django.db.models import F
from django.db.models.aggregates import Count

from apps.managers.settings_mgr import get_round_info
from apps.widgets.energy_goal.models import TeamEnergyGoal
from apps.widgets.energy_scoreboard.models import EnergyData


def supply(request, page_name):
    """Supply the view_objects content.

       :return: team, scoreboard_round, goals_scoreboard, energy_ranks"""
    _ = page_name

    user = request.user
    team = user.get_profile().team

    rounds = get_round_info()
    scoreboard_rounds = []
    today = datetime.datetime.today()
    for key in rounds.keys():
        # Check if this round happened already or if it is in progress.
        # We don't care if the round happens in the future.
        if today >= rounds[key]["start"]:
            scoreboard_rounds.append(key)

    # Generate the scoreboard for energy goals.
    # We could aggregate the energy goals in teams, but there's a bug in Django.
    # See https://code.djangoproject.com/ticket/13461
    goals_scoreboard = TeamEnergyGoal.objects.filter(
        actual_usage__lte=F("goal_usage")
    ).values(
        "team__name"
    ).annotate(completions=Count("team")).order_by("-completions")

    energy_ranks = EnergyData.get_overall_ranks()

    return {
        "team": team,
        "scoreboard_rounds": scoreboard_rounds,
        "goals_scoreboard": goals_scoreboard,
        "energy_ranks": energy_ranks,
        }
