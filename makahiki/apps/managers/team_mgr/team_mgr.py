"""The manager for managing team."""
from django.db.models.aggregates import Sum, Max
from apps.managers.team_mgr.models import Team


def team_members(team):
    """Get the team members."""
    return team.profile_set()


def team_points_leaders(num_results=10, round_name="Overall"):
    """Returns the team points leaders across all groups."""
    return Team.objects.select_related('group').filter(
        profile__scoreboardentry__round_name=round_name
    ).annotate(
        points=Sum("profile__scoreboardentry__points"),
        last=Max("profile__scoreboardentry__last_awarded_submission")
    ).order_by("-points", "-last")[:num_results]
