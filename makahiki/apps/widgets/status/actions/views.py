"""handles the request for action status."""

from django.db.models import Count

from apps.widgets.quests.models import Quest
from apps.widgets.smartgrid.models import ActionMember


def supply(request, page_name):
    """supply the view objects for action status."""
    _ = page_name
    _ = request

    quests = Quest.objects.filter(
        questmember__completed=True,
    ).values("name").annotate(completions=Count("questmember")).order_by("-completions")

    members = ActionMember.objects.filter(
        action__type='activity',
        approval_status='pending',
    ).order_by('submission_date')

    pending_members = members.count()
    oldest_member = None
    if pending_members > 0:
        oldest_member = members[0]

    return {
        "quests": quests,
        "pending_members": pending_members,
        "oldest_member": oldest_member,
        }
