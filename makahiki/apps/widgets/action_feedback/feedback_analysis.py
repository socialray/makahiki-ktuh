"""Provides analysis functions for Action_Feedback widget."""
from apps.widgets.action_feedback.models import ActionFeedback
from apps.widgets.smartgrid.models import Action
from django.db.models.aggregates import Count, Avg


def get_action_feedback(action):
    """returns the feedback for the given action."""
    return ActionFeedback.objects.filter(action=action)


def get_actions_with_feedback():
    """returns the actions with feedback."""
    return Action.objects.annotate(num_feedback=Count('actionfeedback'))\
        .filter(num_feedback__gt=0)\
        .annotate(ave_rating=Avg('actionfeedback__rating'))


def get_feedback_comments(action):
    """returns the user feedback comments for the given action."""
    comments = []
    for feedback in get_action_feedback(action):
        comments.append(feedback.comment)
    return comments


def get_ordered_actions_with_feedback():
    """returns the actions with feedback ordered by level, category, and priority."""
    #with_feedback = get_actions_with_feedback()
    #return with_feedback.order_by('-ave_rating')

    return ActionFeedback.objects.values('action__name', 'action__slug', 'action__type').annotate(
        count=Count('rating'),
        average=Avg('rating')).order_by('-average')


def build_google_chart_data():
    """Builds the data for graphing the feedback in google visualizations."""
    d = {}
    ordered_actions = get_ordered_actions_with_feedback()
    d['height'] = ordered_actions.count() * 35
    action_feedback = []
    for counter, action in enumerate(ordered_actions):
        temp = []
        temp.append(str(action.slug))
        _ = counter
        feedback = get_action_feedback(action)
        temp.append(-feedback.filter(rating=2).count())
        temp.append(-feedback.filter(rating=1).count())
        temp.append(feedback.filter(rating=4).count())
        temp.append(feedback.filter(rating=5).count())
        action_feedback.append(temp)
    d['data'] = action_feedback
    return d


def build_feedback_data():
    """Builds the data for graphing the feedback as a horizontal stacked
    bar chart."""
    d = {}
    ordered_actions = get_ordered_actions_with_feedback()
    d['height'] = ordered_actions.count() * 50
    f_5 = []  # holds data for feedback with score = 5
    f_4 = []  # holds data for feedback with score = 4
    temp = []  # holds data for feedback with score = 3
    f_2 = []  # holds data for feedback with score = 2
    f_1 = []  # holds data for feedback with score = 1
    ticks = []
    max_pos = 0
    max_neg = 0
    for counter, action in enumerate(ordered_actions):
        ticks.append([counter + 1, str("<a href=\"/action_feedback/") +\
                       str(action.type) + "/" + str(action.slug) +\
                       "/view_feedback/\">" + str(action.slug) + "</a>"])
        feedback = get_action_feedback(action)
        if feedback.filter(rating=5).count() +\
         feedback.filter(rating=4).count() > max_pos:
            max_pos = feedback.filter(rating=5).count() +\
                        feedback.filter(rating=4).count()
        f_5.append([feedback.filter(rating=5).count(), 0.7 + counter])
        f_4.append([feedback.filter(rating=4).count(), 0.7 + counter])
        temp.append([feedback.filter(rating=2).count() +\
                      feedback.filter(rating=1).count(), 0.7 + counter])
        if feedback.filter(rating=2).count() +\
         feedback.filter(rating=1).count() > max_neg:
            max_neg = feedback.filter(rating=2).count() +\
                        feedback.filter(rating=1).count()
        f_2.append([-feedback.filter(rating=2).count(), 0.7 + counter])
        f_1.append([-feedback.filter(rating=1).count(), 0.7 + counter])
    d['d5'] = f_5
    d['d4'] = f_4
    d['d3'] = temp
    d['d2'] = f_2
    d['d1'] = f_1
    d['yticks'] = ticks
    ticks = []
    if max_neg > 0:
        ticks.append([-max_neg / 2, 'Negative'])
    if max_pos > 0:
        ticks.append([max_pos / 2, 'Positive'])
    d['xticks'] = ticks
    return d


def get_likert_scale_totals(action):
    """returns the totals for the Likert scale for the given action."""
    query_set = get_action_feedback(action)
# data = []
# {label: 'foo', data: [[1,300], [2,300], [3,300], [4,300], [5,300]]},
# {label: 'bar', data: [[1,800], [2,600], [3,400], [4,200], [5,0]]},
# {label: 'baz', data: [[1,100], [2,200], [3,300], [4,400], [5,500]]},
# ];
    scale = []
# for i in xrange(1,5):
# temp = {}
# temp['label'] = i
# temp['data'] = [query_set.filter(rating=i).count(), 1]
# scale.append(temp)

    scale.append(['1', query_set.filter(rating=1).count()])
    scale.append(['2', query_set.filter(rating=2).count()])
    scale.append(['3', query_set.filter(rating=3).count()])
    scale.append(['4', query_set.filter(rating=4).count()])
    scale.append(['5', query_set.filter(rating=5).count()])
    return scale


def get_feedback_average(action):
    """returns the average feedback rating for the given action."""

    return ActionFeedback.objects.filter(
        action=action).aggregate(avg=Avg('rating'))['avg']
    #query_set = get_action_feedback(action)
    #total = 0
    #for i in xrange(1, 6):
    #    total += query_set.filter(rating=i).count() * i
    #count = query_set.count()
    #if count == 0:
    #    count = 1
    #return 1.0 * total / count


def get_total_feedback_average():
    """returns the average rating of all the feedback."""
    return ActionFeedback.objects.aggregate(avg=Avg('rating'))['avg']
        #running_total = 0
        #for action in get_actions_with_feedback():
        #    running_total += get_feedback_average(action)
        #count = get_actions_with_feedback().count()
        #if count == 0:
        #    count = 1
        #return 1.0 * running_total / count


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
    #analysis['scale'] = get_likert_scale_totals(action)
    analysis['average'] = get_feedback_average(action)
    analysis['count'] = get_action_feedback(action).count()

    return analysis


def get_analysis():
    """returns the feedback analysis for each of the actions as a dictionary
keyed with the action name."""
    analysis = {}
    """
    data = []
    for action in get_ordered_actions_with_feedback():
        data.append(build_analysis(action))
        # analysis[action.name] = build_analysis(action)
    """
    analysis['overall_average'] = get_total_feedback_average()
    analysis['data'] = get_ordered_actions_with_feedback()

    return analysis
