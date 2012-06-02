"""line chart visualization."""

from apps.managers.team_mgr.models import Team


def supply(request, page_name):
    """ Handle the request for viz_chart widget."""

    _ = page_name
    _ = request

    all_lounges = Team.objects.order_by('name').all()

    return  {
        "all_lounges": all_lounges,
        }
