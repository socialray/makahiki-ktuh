"""Implements the Smart Grid Game widget."""

import datetime
from django.db.models import  Count
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from apps.managers.cache_mgr import cache_mgr
from apps.utils import utils
from apps.widgets.smartgrid import NUM_GOLOW_ACTIONS, SETUP_WIZARD_ACTIVITY_NAME
from apps.widgets.smartgrid.models import Action, Category, Activity, ActionMember
from apps.widgets.smartgrid.models import Event
from apps.widgets.smartgrid import  MAX_COMMITMENTS


def complete_setup_activity(user):
    """complete the setup activity."""
    try:
        activity = Activity.objects.get(name=SETUP_WIZARD_ACTIVITY_NAME)
        
        try:
            member = ActionMember.objects.get(
                action=activity,
                user=user)
        except ObjectDoesNotExist:
            member = ActionMember(
                action=activity,
                user=user)

        member.approval_status = "approved"
        member.save()
    except ObjectDoesNotExist:
        pass  # Don't add anything if we can't find to the activity.


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

    #Calculate the task duration
    if action.type != "commitment":
        if action.type == "activity":
            duration = action.activity.duration
        else:
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


def get_category_actions(user):
    """Return the category list with the tasks info"""
    categories = cache_mgr.get_cache('smartgrid-categories-%s' % user.username)
    if not categories:
        categories = Category.objects.all()
        for cat in categories:
            action_list = []
            for action in cat.action_set.all().order_by("priority"):
                action = annotate_action_status(user, action)
                action_list.append(action)

            cat.task_list = action_list

        # Cache the categories for an hour (or until they are invalidated)
        cache_mgr.set_cache('smartgrid-categories-%s' % user,
            categories, 60 * 60)

    return categories


def get_popular_tasks():
    """Returns a dictionary containing the most popular tasks.
       The keys are the type of the task and the values are a list of tasks."""
    return {
        "Activity": get_popular_actions("activity", "approved")[:5],
        "Commitment": get_popular_actions("commitment", "approved")[:5],
        "Event": get_popular_actions("event", "pending")[:5],
        "Excursion": get_popular_actions("excursion", "pending")[:5],
        }


def get_popular_actions(action_type, approval_status):
    """Gets the most popular activities in terms of completions."""
    return Action.objects.filter(actionmember__approval_status=approval_status,
                                 type=action_type,
        ).annotate(completions=Count("actionmember")).order_by("-completions")


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


def get_available_golow_actions(user):
    """Retrieves only the golow activities that a user can participate in (excluding events)."""

    actions = Action.objects.exclude(
        actionmember__user=user,
    ).filter(
        related_resource="energy",
        pub_date__lte=datetime.date.today(),
        expire_date__gte=datetime.date.today(),
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

    categories = cache_mgr.get_cache('smartgrid-categories-%s' % user.username)
    if not categories:
        return eval_unlock(user, action)

    for cat in categories:
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


def eval_unlock(user, action):
    """Determine the unlock status of a task by dependency expression"""
    predicates = action.depends_on
    if not predicates:
        return False

    return utils.eval_predicates(predicates, user, SMARTGRID_PREDICATES)


def has_action(user, slug=None, action_type=None):
    """Determines if the user is participating in a task.

        * For a activity, this returns True if the user submitted or completed the activity.
        * For a commitment, this returns True if the user made or completed the commitment.
        * For a event or excursion, this returns True if the user entered their attendance code.
        * For a survey, this returns True if the user completed the survey.

       If a action_type is specified, then checks to see if a user has completed a task of that type.
       Only one of name and action_type should be specified."""
    if not slug and not action_type:
        raise Exception("Either slug or action_type must be specified.")

    if slug:
        try:
            task = Action.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return False

        return is_pau(user, task)
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
        pub_date__lte=datetime.date.today(),
        expire_date__gte=datetime.date.today(),
        event_date__gte=datetime.date.today(),
    ).order_by("event_date")

    unlock_events = []
    for event in events:
        if is_unlock(user, event) and not event.is_event_completed():
            unlock_events.append(event)

    return unlock_events
