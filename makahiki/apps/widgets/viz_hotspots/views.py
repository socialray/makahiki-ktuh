"""hotspots visualization."""

from apps.managers.team_mgr.models import Team


def supply(request, page_name):
    """ Handle the request for viz_hotspots widget."""

    _ = request
    _ = page_name

    all_lounges = Team.objects.order_by('name').all()

    return  {
        "all_lounges": all_lounges,
        }
