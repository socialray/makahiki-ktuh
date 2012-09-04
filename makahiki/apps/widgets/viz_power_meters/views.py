"""Power meters visualization."""

from apps.managers.team_mgr.models import Team


def supply(request, page_name):
    """ Handle the viz request."""

    _ = page_name

    team = request.user.get_profile().team
    group_lounges_count = 5
    all_lounges = Team.objects.order_by('name').all()
    group_lounges_list = []

    if team:
        group_lounges = team.group.team_set.order_by('name').all()[:group_lounges_count]
        remainer = group_lounges_count - group_lounges.count()
        if remainer:
            remainer_lounges = Team.objects.exclude(group=team.group).order_by('name')[:remainer]
            if remainer_lounges.count():
                for l in group_lounges:
                    group_lounges_list.append(l)
                for l in remainer_lounges:
                    group_lounges_list.append(l)
    else:
        group_lounges = all_lounges[:group_lounges_count]

    if group_lounges_list:
        group_lounges = group_lounges_list
        group_lounges_count = len(group_lounges)
    else:
        group_lounges_count = group_lounges.count()

    return  {
        "all_lounges": all_lounges,
        "group_lounges": group_lounges,
        "group_lounges_count": group_lounges_count,
        }


def remote_supply(request, page_name):
    """ Supports remote requests."""
    return supply(request, page_name)
