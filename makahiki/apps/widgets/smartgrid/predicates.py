"""Predicates indicating if a level or cell should be unlocked."""

from datetime import datetime, timedelta
from django.db.models.query_utils import Q
from apps.widgets.smartgrid import smartgrid
from apps.widgets.smartgrid.models import Action, Event


def completed_action(user, slug):
    """Returns true if the user complete the action."""
    return slug in smartgrid.get_completed_actions(user)


def completed_all_of(user, category_slug=None, action_type=None, resource=None, level_name=None):
    """Returns true if completed all of the specified type."""

    if category_slug:
        count = Action.objects.filter(category__slug=category_slug).count()
        return not count and \
               user.actionmember_set.filter(action__category__slug=category_slug).count() == count

    if action_type:
        count = Action.objects.filter(type=action_type).count()
        return not count and \
               user.actionmember_set.filter(action__type=action_type).count() == count

    if resource:
        count = Action.objects.filter(related_resource=resource).count()
        return not count and \
               user.actionmember_set.filter(action__related_resource=resource).count() == count

    if level_name:
        count = Action.objects.filter(level__name=level_name).count()
        return not count and \
               user.actionmember_set.filter(action__level__name=level_name).count() == count

    count = Action.objects.all().count()
    return not count and user.actionmember_set.all().count() == count


def completed_some_of_level(user, some=1, level_name=None):
    """Returns true if completed some of the specified level."""
    return completed_some_of(user, some=some, level_name=level_name)


def completed_some_full_spectrum(user, some=1):
    """Returns true if the user has completed some activities, commitments, and
    events."""
    ret = completed_some_of(user, some=some, action_type='activity')
    ret = ret and completed_some_of(user, some=some, action_type='commitment')
    ret = ret and completed_some_of(user, some=some, action_type='event')
    return ret


def completed_some_of(user, some=1, category_slug=None, action_type=None, resource=None,
                      level_name=None):
    """Returns true if completed some of the specified type.
    some is default to 1 if not specified."""
    if category_slug:
        return user.actionmember_set.filter(action__category__slug=category_slug).count() >= some

    if action_type:
        return user.actionmember_set.filter(action__type=action_type).count() >= some

    if resource:
        return user.actionmember_set.filter(action__related_resource=resource).count() >= some

    if level_name:
        return user.actionmember_set.filter(action__level__name=level_name).count() >= some

    return user.actionmember_set.all().count() >= some


def completed_level(user, lvl=1):
    """Returns true if the user has performed all activities successfully, and
      attempted all commitments."""
    num_completed = user.actionmember_set.filter(
        Q(action__type='activity') | Q(action__type='commitment'),
        action__level__priority=lvl).count()
    num_level = Action.objects.filter(
        Q(type='activity') | Q(type='commitment'),
        level__priority=lvl).count()

    # check if there is any activity or commitment
    if not num_level:
        return False

    return num_completed == num_level


def unlock_on_date(user, date_string):
    """Returns true if the current date is equal to or after the date_string."""
    _ = user
    today = datetime.today()
    unlock_date = datetime.strptime(date_string, "%m/%d/%y")
    return today >= unlock_date


def unlock_on_event(user, event_slug, days=0, lock_after_days=0):
    """Returns true if the current date is equal to or after the date of the Event
    defined by the event_slug, optionally days before. days should be a negative number.
    Optionally lock_after_days, if not zero then will return false lock_after_days
    after the event."""
    _ = user
    today = datetime.today()
    day_delta = timedelta(days=days)
    event = Event.objects.get(slug=event_slug)
    if event:
        unlock_date = event.event_date + day_delta
        if lock_after_days != 0:
            day_after = timedelta(days=lock_after_days)
            lock_date = event.event_date + day_after
            return today >= unlock_date and today <= lock_date
        else:
            return today >= unlock_date
    else:
        return True


def approved_action(user, slug):
    """Returns true if the action is approved."""
    return user.actionmember_set.filter(action__slug=slug, approval_status="approved").count() > 0


def approved_some_of(user, some=1, category_slug=None, action_type=None, resource=None,
                     level_name=None):
    """Returns true if some actions of the specified type is approved."""

    if category_slug:
        return user.actionmember_set.filter(action__category__slug=category_slug,
                                            approval_status="approved").count() >= some

    if action_type:
        return user.actionmember_set.filter(action__type=action_type,
                                            approval_status="approved").count() >= some

    if resource:
        return user.actionmember_set.filter(action__related_resource=resource,
                                            approval_status="approved").count() >= some

    if level_name:
        return user.actionmember_set.filter(action__level__name=level_name,
                                            approval_status="approved").count() >= some

    return user.actionmember_set.filter(approval_status="approved").count() >= some


def approved_all_of(user, category_slug=None, action_type=None, resource=None, level_name=None):
    """Returns true if all actions of the specified type is approved."""

    if category_slug:
        count = Action.objects.filter(category__slug=category_slug).count()
        return not count and user.actionmember_set.filter(action__category__slug=category_slug,
                                            approval_status="approved").count() == count

    if action_type:
        count = Action.objects.filter(type=action_type).count()
        return not count and user.actionmember_set.filter(action__type=action_type,
                                            approval_status="approved").count() == count

    if resource:
        count = Action.objects.filter(related_resource=resource).count()
        return not count and user.actionmember_set.filter(action__related_resource=resource,
                                            approval_status="approved").count() == count

    if level_name:
        count = Action.objects.filter(level__name=level_name).count()
        return not count and user.actionmember_set.filter(action__level__name=level_name,
                                            approval_status="approved").count() == count

    count = Action.objects.all().count()
    return not count and user.actionmember_set.filter(approval_status="approved").count() == count


def social_bonus_count(user, count):
    """Returns True if the number of social bonus the user received equals to count."""
    return user.actionmember_set.filter(social_bonus_awarded=True).count() >= count
