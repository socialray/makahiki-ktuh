"""Provides predicate functions for runtime condition evaluation."""
from apps.widgets.smartgrid.models import Action, Category


def completed_action(user, slug):
    """Returns true if the user complete the action."""
    return user.actionmember_set.filter(action__slug=slug).count() > 0


def completed_all_of_category(user, slug):
    """Returns true if completed all of the category."""
    return user.actionmember_set.filter(action__category__slug=slug).count() ==\
           Category.objects.filter(slug=slug).count()


def completed_some_of_category(user, slug, some=1):
    """Returns true if completed some of the category. some is default to 1 if not specified."""
    return user.actionmember_set.filter(action__category__slug=slug).count() >= some


def completed_some_of_type(user, type, some=1):
    """Returns true if completed some of the action type. some is default to 1 if not specified."""
    return user.actionmember_set.filter(action__type=type).count() > some


def completed_all_of_type(user, type):
    """Returns true if completed some of the action type. some is default to 1 if not specified."""
    return user.actionmember_set.filter(action__type=type).count() ==\
           Action.objects.filter(type=type).count()


def action_approved(user, slug):
    """Returns true if the action is approved."""
    return user.actionmember_set.filter(
            action__slug=slug,
            approval_status="approved",
        ).count() > 0
