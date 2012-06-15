"""Views handler for action_feedback rendering."""

import datetime


#from apps.widgets.action_feedback.models import ActionFeedback
from apps.widgets.action_feedback import feedback_analysis
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from apps.widgets.smartgrid import smartgrid
from apps.widgets.action_feedback.models import ActionFeedback
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from apps.widgets.action_feedback.forms import ActionFeedbackForm
from django.shortcuts import render_to_response
from django.template.context import RequestContext
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


@never_cache
@login_required
def action_feedback(request, action_type, slug):
    """Handle feedback for an action."""
    _ = action_type
    action = smartgrid.get_action(slug=slug)
    user = request.user

    form = ActionFeedbackForm(request.POST)
    if form.is_valid():
        print form.cleaned_data

    feedback = ActionFeedback()
    feedback.user = user
    feedback.action = action
    feedback.rating = request.POST['Score']
    feedback.comment = request.POST['comments']
    feedback.added = datetime.datetime.now()
    feedback.changed = datetime.datetime.now()
    feedback.save()
    # Take them back to the action page.
    return HttpResponseRedirect(reverse("activity_task", args=(action.type, action.slug,)))


@never_cache
@login_required
def view_feedback(request, action_type, slug):
    """view the detailed feedback for the action."""
    _ = action_type
    action = smartgrid.get_action(slug)

    return render_to_response("feedback_details.html", {
        "action": action,
        "feedback": feedback_analysis.get_action_feedback(action),
        "scale": feedback_analysis.get_likert_scale_totals(action)
        }, context_instance=RequestContext(request))
