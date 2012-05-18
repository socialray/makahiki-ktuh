"""Handle the rendering of the energy scoreboard widget."""

from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.resource_mgr import resource_mgr
from apps.widgets.resource_goal import resource_goal


def supply(request, page_name):
    """Supply the view_objects content."""
    _ = request
    _ = page_name
    return {}


def resource_supply(request, resource):
    """Supply the view_objects content.
       :return: team, goals_scoreboard, resource_round_ranks"""

    user = request.user
    team = user.get_profile().team

    rounds = challenge_mgr.get_round_info()
    round_resource_ranks = {}
    for key in rounds.keys():
        ranks = resource_mgr.resource_ranks(resource, key)
        if ranks:
            round_resource_ranks[key] = ranks

    goals_scoreboard = resource_goal.resource_goal_ranks(resource)

    resource_settings = resource_mgr.get_resource_settings(resource)

    return {
        "team": team,
        "resource": resource_settings,
        "goals_scoreboard": goals_scoreboard,
        "round_resource_ranks": round_resource_ranks,
        }
