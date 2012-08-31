"""Provides the view of the team member widget."""

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from apps.managers.team_mgr import team_mgr


def supply(request, page_name):
    """Supply view_objects content, which is the set of team members."""
    _ = page_name

    # Get the team members.
    team = request.user.get_profile().team
    if team:
        members_with_points = []
        zero_point_members = []
        for member in team_mgr.team_members(team):
            if member.setup_complete:
                members_with_points.append(member)
            else:
                zero_point_members.append(member)
    else:
        members_with_points = None
        zero_point_members = None

    return {
        "team_members": members_with_points,
        "zero_members": zero_point_members,
        }


@never_cache
@login_required
def team_members(request):
    """Provide the team members."""
    team = request.user.get_profile().team
    if team:
        members = team_mgr.team_members(team)
    else:
        members = None

    return render_to_response("team_members.html", {
        "team_members": members,
        }, context_instance=RequestContext(request))
