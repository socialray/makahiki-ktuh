"""Provides analysis functions for Action_Feedback widget."""
from apps.widgets.action_feedback.models import ActionFeedback
from apps.widgets.smartgrid.models import Action
from django.db.models.aggregates import Count


def get_action_feedback(action):
    """returns the feedback for the given action."""
    return ActionFeedback.objects.filter(action=action)


def get_actions_with_feedback():
    """returns the actions with feedback."""
    return Action.objects.annotate(num_feedback=Count('actionfeedback')).filter(num_feedback__gt=0)


def get_feedback_comments(action):
    """returns the user feedback comments for the given action."""
    comments = []
    for feedback in get_action_feedback(action):
        comments.append(feedback.comment)
    return comments


def get_likert_scale_totals(action):
    """returns the totals for the Likert scale for the given action."""
    query_set = get_action_feedback(action)
    scale = []
    scale.append([0.7, query_set.filter(rating=1).count()])
    scale.append([1.7, query_set.filter(rating=2).count()])
    scale.append([2.7, query_set.filter(rating=3).count()])
    scale.append([3.7, query_set.filter(rating=4).count()])
    scale.append([4.7, query_set.filter(rating=5).count()])
    return scale


def get_action_likert_scales():
    """returns the likert scale feedback as a dictionary with the action name as key."""
    ret = {}
    for action in get_actions_with_feedback():
        ret[action.name] = get_likert_scale_totals(action)
    return ret
