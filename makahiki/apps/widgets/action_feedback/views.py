"""Views handler for action_feedback rendering."""
#from apps.widgets.action_feedback.models import ActionFeedback
from apps.widgets.action_feedback import feedback_analysis
#from apps.widgets.smartgrid.models import Action
#from django.db.models.aggregates import Count


def supply(request, page_name):
    """Supply view_objects for the Action_Feedback template."""
    _ = page_name
    _ = request

    return {
        "action_feedback": feedback_analysis.get_action_likert_scales(),
        "analysis": feedback_analysis.get_analysis()
    }
