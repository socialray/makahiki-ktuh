"""Prepares the views for participation widget."""
from apps.managers.team_mgr.models import Team
from apps.widgets.participation.models import TeamParticipation


def supply(request, page_name):
    """Supply the view_objects content for this widget, which is participation data."""

    _ = request
    _ = page_name
    num_results = 10
    team_participation = TeamParticipation.objects.all()[:num_results]
    if not team_participation:
        team_participation = Team.objects.all()[:num_results]
        for t in team_participation:
            t.team = t
            t.participation = 0

    return {
        "team_participation": team_participation,
    }


def remote_supply(request, page_name):
    """Supplies data to remote views."""
    return supply(request, page_name)
