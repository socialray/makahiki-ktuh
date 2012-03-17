"""Provides the view of the team member widget."""

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User

from apps.managers.player_mgr.models import Profile


def supply(request, page_name):
    """Supply view_objects content, which is the set of team members."""
    _ = page_name
    team_id = request.user.get_profile().team_id

    # Get the team members.
    members = Profile.objects.filter(team=team_id).order_by(
        "-points",
        "-last_awarded_submission"
    ).select_related('user')[:12]

    return {
        "team_members": members,
        }


@never_cache
@login_required
def team_members(request):
    """Provide the team members."""
    members = User.objects.filter(profile__team=request.user.get_profile().team).order_by(
        "-profile__points",
        "-profile__last_awarded_submission",
    )

    return render_to_response("team_members.html", {
        "team_members": members,
        }, context_instance=RequestContext(request))
