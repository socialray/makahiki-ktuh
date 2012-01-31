from django.shortcuts import  render_to_response
from django.db.models import Count

from managers.base_mgr import get_current_round
from widgets.smartgrid.models import *
from widgets.smartgrid import *
from managers.team_mgr.models import *
from managers.team_mgr import *
from managers.player_mgr.models import *
from managers.player_mgr import *

def supply(request):
    user = request.user

    floor = user.get_profile().floor
    user_floor_standings = None

    current_round = get_current_round()
    round_name = current_round if current_round else None
    floor_standings = Floor.floor_points_leaders(num_results=10, round_name=round_name)
    profile_standings = Profile.points_leaders(num_results=10, round_name=round_name)
    if floor:
        user_floor_standings = floor.points_leaders(num_results=10, round_name=round_name)

    # Calculate active participation.
    floor_participation = Floor.objects.filter(profile__points__gte=50).annotate(
        user_count=Count('profile'),
    ).order_by('-user_count').select_related('dorm')[:10]

    for f in floor_participation:
        f.active_participation = (f.user_count * 100) / f.profile_set.count()

    return {
        "profile":user.get_profile(),
        "floor": floor,
        "current_round": round_name or "Overall",
        "floor_standings": floor_standings,
        "profile_standings": profile_standings,
        "user_floor_standings": user_floor_standings,
        "floor_participation": floor_participation, }
