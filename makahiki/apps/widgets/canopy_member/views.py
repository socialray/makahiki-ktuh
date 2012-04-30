"""Handles request for Canopy member"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import never_cache
from apps.managers.player_mgr import player_mgr


def supply(request, page_name):
    """Handle canopy member request."""

    _ = page_name

    # Load members
    canopy_members = player_mgr.canopy_members()

    # Check for the about cookie.
    hide_about = False
    if "hide-about" in request.COOKIES:
        hide_about = True

    return  {
        "members": canopy_members,
        "hide_about": hide_about,
        }


@login_required
@never_cache
def members(request):
    """
    Lists all of the members of the canopy.
    """
    canopy_members = player_mgr.canopy_members()

    return render_to_response("canopy_members.html", {
        "in_canopy": True,
        "members": canopy_members,
        }, context_instance=RequestContext(request))
