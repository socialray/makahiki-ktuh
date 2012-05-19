"""handles the request for action status."""

from django.db.models import Count

from apps.widgets.quests.models import Quest
from apps.widgets.smartgrid import smartgrid
from apps.widgets.smartgrid.models import ActionMember, Action


def supply(request, page_name):
    """supply the view objects for action status."""
    _ = page_name
    _ = request

    popular_tasks = {}
    for type_choice in Action.TYPE_CHOICES:
        action_type = type_choice[0]
        task_list = []
        actions = smartgrid.get_popular_action_submissions(action_type)
        for action in actions:
            task = {"type": action.type,
                    "slug": action.slug,
                    "title": action.title,
                    "completions": ActionMember.objects.filter(action=action,
                                                               approval_status="approved").count(),
                    "submissions": action.submissions,
                    }
            task_list.append(task)
        popular_tasks[action_type] = task_list

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
        "popular_tasks": popular_tasks,
        "quests": quests,
        "pending_members": pending_members,
        "oldest_member": oldest_member,
        }
