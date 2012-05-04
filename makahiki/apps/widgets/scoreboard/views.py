"""Prepares the views for point scoreboard widget."""

from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.player_mgr import player_mgr
from apps.managers.team_mgr import team_mgr


def supply(request, page_name):
    """Supply the view_objects content for this widget, which is all the scoreboard data."""

    _ = page_name
    user = request.user

    team = user.get_profile().team
    user_team_standings = None

    current_round = challenge_mgr.get_current_round()
    round_name = current_round if current_round else None
    team_standings = team_mgr.team_points_leaders(num_results=10, round_name=round_name)
    profile_standings = player_mgr.points_leaders(num_results=10, round_name=round_name)
    if team:
        user_team_standings = team.points_leaders(num_results=10, round_name=round_name)

    team_participation = team_mgr.team_active_participation()

    return {
        "profile": user.get_profile(),
        "team": team,
        "current_round": round_name or "Overall",
        "team_standings": team_standings,
        "profile_standings": profile_standings,
        "user_team_standings": user_team_standings,
        "team_participation": team_participation, }
