"""Prepares the views for point scoreboard widget."""

from django.db.models.aggregates import Count
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.player_mgr import player_mgr
from apps.managers.team_mgr import team_mgr
from apps.managers.team_mgr.models import Team


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

    # Calculate active participation.
    team_participation = Team.objects.filter(
        profile__scoreboardentry__points__gte=50,
        profile__scoreboardentry__round_name="Overall").annotate(
            user_count=Count('profile')).order_by('-user_count').select_related('group')[:10]

    for f in team_participation:
        f.active_participation = (f.user_count * 100) / f.profile_set.count()

    return {
        "profile": user.get_profile(),
        "team": team,
        "current_round": round_name or "Overall",
        "team_standings": team_standings,
        "profile_standings": profile_standings,
        "user_team_standings": user_team_standings,
        "team_participation": team_participation, }
