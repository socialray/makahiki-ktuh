"""Handle the rendering of the energy scoreboard widget."""

import datetime
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.resource_mgr import resource_mgr


def supply(request, page_name):
    """Supply the view_objects content."""
    _ = request
    _ = page_name
    return {}


def resource_supply(request, resource):
    """Supply the view_objects content.

       :return: team, scoreboard_round, goals_scoreboard, energy_ranks"""

    user = request.user
    team = user.get_profile().team

    rounds = challenge_mgr.get_round_info()
    scoreboard_rounds = []
    today = datetime.datetime.today()
    for key in rounds.keys():
        # Check if this round happened already or if it is in progress.
        # We don't care if the round happens in the future.
        if today >= rounds[key]["start"]:
            scoreboard_rounds.append(key)

    goals_scoreboard = resource_mgr.energy_goal_ranks()

    energy_ranks = resource_mgr.resource_ranks(resource)

    resource_settings = resource_mgr.get_resource_settings(resource)
    return {
        "team": team,
        "resource": resource_settings,
        "scoreboard_rounds": scoreboard_rounds,
        "goals_scoreboard": goals_scoreboard,
        "energy_ranks": energy_ranks,
        }
