"""Implements the Smart Grid Game widget."""

import datetime
from django.db.models import  Count
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Max
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404
from apps.managers.cache_mgr import cache_mgr
from apps.utils import utils
from apps.widgets.smartgrid import NUM_GOLOW_ACTIONS, SETUP_WIZARD_ACTIVITY
from apps.widgets.smartgrid.models import Action, Category, ActionMember
from apps.widgets.smartgrid.models import Event
from apps.widgets.smartgrid import  MAX_COMMITMENTS


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
    action.is_pau = is_pau(user, action)

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
        max_level = Action.objects.all().aggregate(Max('level'))['level__max']

        levels = []
        if max_level:
            for level in range(0, max_level):
                categories = Category.objects.all()
                for cat in categories:
                    action_list = []
                    for action in cat.action_set.filter(level=level + 1).order_by("priority"):
                        action = annotate_action_status(user, action)
                        action_list.append(action)

                    cat.task_list = action_list
                levels.append(categories)

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


def is_pau(user, action):
    """Return true if the task is done for the user."""
    members = ActionMember.objects.filter(user=user, action=action)
    if members:
        return True
    else:
        return False


def completed(user, action_slug):
    """Return true if the user complete the action."""
    actions = Action.objects.filter(slug=action_slug)
    if actions:
        return is_pau(user, actions[0])
    else:
        return False


def completedAllOf(user, cat_slug):
    """Return true if completed all of the category."""
    try:
        cat = Category.objects.get(slug=cat_slug)
    except ObjectDoesNotExist:
        return False

    for action in cat.action_set.all():
        if not is_pau(user, action):
            return False

    return True


def completedSomeOf(user, some, cat_slug):
    """Return true if completed some of the category."""
    try:
        cat = Category.objects.get(slug=cat_slug)
    except ObjectDoesNotExist:
        return False

    count = 0
    for action in cat.action_set.all():
        if is_pau(user, action):
            count = count + 1
        if count == some:
            return True

    return False


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


SMARTGRID_PREDICATES = {
    "completedAllOf": completedAllOf,
    "completedSomeOf": completedSomeOf,
    "completed": completed,
    "afterPublished": afterPublished,
    }


SMARTGRID_ACTION_PREDICATES = (
    "completed",
    "afterPublished",
    )


def eval_unlock(user, action):
    """Determine the unlock status of a task by dependency expression"""
    predicates = action.depends_on
    if not predicates:
        return False

    # append the action to the predicate parameter
    for name in SMARTGRID_ACTION_PREDICATES:
        predicates = predicates.replace(name + "()", name + "('" + action.slug + "')")

    return utils.eval_predicates(predicates,
                                 user,
                                 SMARTGRID_PREDICATES)


def has_action(user, slug=None, name=None, action_type=None):
    """Determines if the user is participating in a task.

        * For a activity, this returns True if the user submitted or completed the activity.
        * For a commitment, this returns True if the user made or completed the commitment.
        * For a event or excursion, this returns True if the user entered their attendance code.
        * For a survey, this returns True if the user completed the survey.

       If a action_type is specified, then checks to see if a user has completed a task of that type.
       Only one of name and action_type should be specified."""
    if not slug and not action_type and not name:
        raise Exception("Either slug, name or action_type must be specified.")

    if slug or name:
        try:
            if slug:
                action = Action.objects.get(slug=slug)
            if name:
                action = Action.objects.get(name=name)
        except ObjectDoesNotExist:
            return False

        return is_pau(user, action)
    else:
        action_type = action_type.lower()
        return user.actionmember_set.filter(action__type=action_type).count() > 0


def completed_action(user, slug=None, action_type=None):
    """Determines if the user has completed the named task or completed a task of the given type.
       In general, if a user-task member is approved or has an award date, it is completed.
       Only one of name and action_type should be specified.  Specifying neither raises an Exception.
       Specifying both results in an error."""
    if not slug and not action_type:
        raise Exception("Either name or action_type must be specified.")

    if action_type:
        action_type = action_type.lower()

        return user.actionmember_set.filter(
            action__type=action_type,
            approval_status="approved",
        ).count() > 0

    if slug:
        action = Action.objects.get(slug=slug)

        return user.actionmember_set.filter(
            action=action,
            approval_status="approved",
        ).count() > 0


def num_actions_completed(user, num_tasks, category_name=None, action_type=None):
    """Returns True if the user has completed the requested number of tasks."""
    # Check if we have a type and/or category.
    if action_type:
        action_type = action_type.lower()

    category = None
    if category_name:
        category = Category.objects.get(name=category_name)

    user_completed = 0
    if not action_type or action_type != "commitment":
        # Build the query for non-commitment tasks.
        query = ActionMember.objects.filter(
            user=user,
            award_date__isnull=False,
        )

        if action_type:
            query.filter(action__type=action_type)

        if category:
            query.filter(action__category=category)

        user_completed += query.count()

    return user_completed >= num_tasks


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
