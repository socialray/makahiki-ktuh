"""Implements the Smart Grid Game widget."""

import datetime
from django.db.models import  Count
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404
from apps.managers.cache_mgr import cache_mgr
from apps.utils import utils
from apps.widgets.smartgrid import NUM_GOLOW_ACTIONS, SETUP_WIZARD_ACTIVITY
from apps.widgets.smartgrid.models import Action, Category, ActionMember, Level
from apps.widgets.smartgrid.models import Event
from apps.widgets.smartgrid import  MAX_COMMITMENTS
from apps.widgets.smartgrid.predicates import completed_action


def get_setup_activity():
    """Returns the setup activity object."""
    return get_object_or_404(Action, slug=SETUP_WIZARD_ACTIVITY)


def complete_setup_activity(user):
    """complete the setup activity."""

    # error out if we can't find to the activity.
    activity = get_setup_activity()
    members = ActionMember.objects.filter(user=user, action=activity)
    if not members:
        # if points not awarded, do so.
        member = ActionMember(action=activity, user=user)
        member.approval_status = "approved"
        member.save()


def get_action(slug):
    """returns the action object by slug."""
    return get_object_or_404(Action, slug=slug)


def annotate_action_status(user, action):
    """retrieve the action status for the user."""
    action.is_unlock = is_unlock(user, action)
    action.completed = completed_action(user, action.slug)

    members = ActionMember.objects.filter(user=user, action=action)
    if members:
        action.member = members[0]
    else:
        action.member = None

    # calculate the task duration
    if action.type == "commitment":
        action.duration = action.commitment.duration
    else:
        if action.type == "activity":
            duration = action.activity.duration
        else:  # is event
            duration = action.event.duration

        hours = duration / 60
        minutes = duration % 60
        action.duration = ""
        if hours > 1:
            action.duration = "%d hours" % hours
        elif hours > 0:
            action.duration = "%d hour" % hours
        if minutes > 0:
            action.duration += " %d minutes" % minutes

    return action


def get_action_members(action):
    """returns the members that had done the action."""
    return ActionMember.objects.filter(action=action)



def get_level_actions(user):
    """Return the level list with the action info in categories"""
    levels = cache_mgr.get_cache('smartgrid-levels-%s' % user.username)
    if not levels:
        levels = []
        for level in Level.objects.all().order_by("priority"):
            level.is_unlock = utils.eval_predicates(level.unlock_condition, user)

            if level.is_unlock:
                categories = []
                for cat in Category.objects.all().order_by("priority"):
                    action_list = []
                    for action in cat.action_set.filter(level=level).order_by("priority"):
                        action = annotate_action_status(user, action)
                        action_list.append(action)
                    if action_list:
                        cat.task_list = action_list
                        categories.append(cat)

                if categories:
                    level.cat_list = categories

            levels.append(level)

        # Cache the categories for an hour (or until they are invalidated)
        cache_mgr.set_cache('smartgrid-levels-%s' % user,
            levels, 60 * 60)

    return levels


def get_popular_actions(action_type, approval_status, num_results=None):
    """Gets the most popular activities in terms of completions."""
    results = Action.objects.filter(actionmember__approval_status=approval_status,
                                 type=action_type,
        ).annotate(completions=Count("actionmember")).order_by("-completions")

    return results[:num_results] if num_results else results


def get_popular_action_submissions(action_type, num_results=None):
    """Gets the most popular activities in terms of completions."""
    results = Action.objects.filter(type=action_type,
                                    actionmember__approval_status__isnull=False,
        ).annotate(submissions=Count("actionmember")).order_by("-submissions")

    return results[:num_results] if num_results else results


def get_in_progress_members(user):
    """Get the user's incomplete activity members."""
    return user.actionmember_set.filter(
        award_date=None,
    ).order_by("submission_date")


def get_current_commitment_members(user):
    """Get the user's incomplete commitment members."""
    return user.actionmember_set.filter(
        action__type="commitment",
        award_date=None,
    ).order_by("submission_date")


def get_available_golow_actions(user, related_resource):
    """Retrieves only the golow activities that a user can participate in (excluding events)."""

    actions = Action.objects.exclude(
        actionmember__user=user,
    ).filter(
        Q(expire_date__isnull=True) | Q(expire_date__gte=datetime.date.today()),
        related_resource=related_resource,
        pub_date__lte=datetime.date.today(),
    ).order_by("type", "priority")

    # pick one activity per type, until reach NUM_GOLOW_ACTIONS
    action_type = None
    golow_actions = []
    for action in actions:
        if action_type == action.type:
            continue

        if is_unlock(user, action):
            golow_actions.append(action)
            action_type = action.type

            if len(golow_actions) == NUM_GOLOW_ACTIONS:
                break

    return golow_actions


def afterPublished(user, action_slug):
    """Return true if the event/excursion has been published"""
    _ = user
    actions = Action.objects.filter(slug=action_slug)
    if actions:
        return actions[0].pub_date <= datetime.date.today()
    else:
        return False


def is_unlock(user, action):
    """Returns the unlock status of the user action."""
    levels = cache_mgr.get_cache('smartgrid-levels-%s' % user.username)
    if not levels:
        return eval_unlock(user, action)

    for level in levels:
        for cat in level:
            if cat.id == action.category_id:
                for t in cat.task_list:
                    if t.id == action.id:
                        return t.is_unlock

    return False


def eval_unlock(user, action):
    """Determine the unlock status of a task by dependency expression"""
    predicates = action.unlock_condition
    if not predicates:
        return False

    # after published is the default unlock rule for action
    if not afterPublished(user, action.slug):
        return False

    return utils.eval_predicates(predicates,
                                 user)


def can_add_commitment(user):
    """Determines if the user can add additional commitments."""
    return ActionMember.objects.filter(user=user, action__type="commitment",
        award_date__isnull=True).count() < MAX_COMMITMENTS


def can_complete_commitment(user, commitment):
    """Determines if the user can complete commitments, assuming there is a pending commitment"""
    pendings = ActionMember.objects.filter(user=user, action=commitment, award_date=None)

    if pendings:
        return pendings[0].days_left() == 0
    else:
        return False


def get_available_events(user):
    """Retrieves only the events that a user can participate in."""

    events = Event.objects.filter(
        Q(expire_date__isnull=True) | Q(expire_date__gte=datetime.date.today()),
        pub_date__lte=datetime.date.today(),
        event_date__gte=datetime.date.today(),
    ).order_by("event_date")

    unlock_events = []
    for event in events:
        if is_unlock(user, event) and not event.is_event_completed():
            unlock_events.append(event)

    return unlock_events
