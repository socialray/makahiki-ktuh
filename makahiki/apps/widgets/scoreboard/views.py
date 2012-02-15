from django.db.models.aggregates import Count
from managers.settings_mgr import get_current_round
from managers.player_mgr.models import Profile
from managers.team_mgr.models import Team

def supply(request):
    user = request.user

    team = user.get_profile().team
    user_team_standings = None

    current_round = get_current_round()
    round_name = current_round if current_round else None
    team_standings = Team.team_points_leaders(num_results=10, round_name=round_name)
    profile_standings = Profile.points_leaders(num_results=10, round_name=round_name)
    if team:
        user_team_standings = team.points_leaders(num_results=10, round_name=round_name)

    # Calculate active participation.
    team_participation = Team.objects.filter(profile__points__gte=50).annotate(
        user_count=Count('profile'),
    ).order_by('-user_count').select_related('group')[:10]

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
