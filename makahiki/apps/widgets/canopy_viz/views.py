"""Canopy visualization."""

from apps.managers.team_mgr.models import Team, Group


def supply(request, page_name):
    """ Handle the viz request."""

    _ = page_name

    viz = request.REQUEST.get("viz", None)

    all_lounges = Team.objects.order_by('name').all()
    all_groups = Group.objects.order_by('name').all()

    for group in all_groups:
        group.teams = group.team_set.order_by('-name').all()

    if request.user.get_profile().team:
        group_lounges = request.user.get_profile().team.group.team_set.all()
    else:
        group_lounges = all_lounges[:5]

    return  {
        "viz": viz,
        "all_lounges": all_lounges,
        "group_lounges": group_lounges,
        "all_groups": all_groups,
        }
