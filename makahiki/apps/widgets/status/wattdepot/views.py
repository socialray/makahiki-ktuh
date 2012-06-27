"""Power meters visualization."""

from apps.managers.team_mgr.models import Team


def supply(request, page_name):
    """ Handle the viz request."""

    _ = page_name
    _ = request

    all_lounges = Team.objects.order_by('name').all()

    if request.user.get_profile().team:
        group_lounges = request.user.get_profile().team.group.team_set.all()
    else:
        group_lounges = all_lounges[:5]

    return  {
        "group_lounges": group_lounges,
        "all_lounges": all_lounges,
        }
