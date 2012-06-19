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
#    data = []
#        {label: 'foo', data: [[1,300], [2,300], [3,300], [4,300], [5,300]]},
#        {label: 'bar', data: [[1,800], [2,600], [3,400], [4,200], [5,0]]},
#        {label: 'baz', data: [[1,100], [2,200], [3,300], [4,400], [5,500]]},
#    ];
    scale = []
#    for i in xrange(1,5):
#        temp = {}
#        temp['label'] = i
#        temp['data'] = [query_set.filter(rating=i).count(), 1]
#        scale.append(temp)

    scale.append([0.7, query_set.filter(rating=1).count()])
    scale.append([1.7, query_set.filter(rating=2).count()])
    scale.append([2.7, query_set.filter(rating=3).count()])
    scale.append([3.7, query_set.filter(rating=4).count()])
    scale.append([4.7, query_set.filter(rating=5).count()])
    return scale


def get_feedback_average(action):
    """returns the average feedback rating for the given action."""
    query_set = get_action_feedback(action)
    count = query_set.count()
    if count == 0:
        count = 1
    total = 0
    for i in xrange(1, 6):
        total += query_set.filter(rating=i).count() * i
    return total / count


def get_total_feedback_average():
    """returns the average rating of all the feedback."""
    running_total = 0
    for action in get_actions_with_feedback():
        running_total += get_feedback_average(action)
    return running_total / get_actions_with_feedback().count()


def get_action_likert_scales():
    """returns the likert scale feedback as a dictionary with the action name as key."""
    ret = {}
    for action in get_actions_with_feedback():
        ret[action.name] = get_likert_scale_totals(action)
        #ret[action.name + 'ave'] = get_feedback_average(action)
    return ret


def build_analysis(action):
    """creates the feedback analysis for the given action."""
    analysis = {}
    analysis['action'] = action
    analysis['scale'] = get_likert_scale_totals(action)
    analysis['average'] = get_feedback_average(action)
    analysis['count'] = get_action_feedback(action).count()
    return analysis


def get_analysis():
    """returns the feedback analysis for each of the actions as a dictionary
    keyed with the action name."""
    analysis = {}
    for action in get_actions_with_feedback():
        analysis[action.name] = build_analysis(action)
    analysis['overall_average'] = get_total_feedback_average()
    return analysis
