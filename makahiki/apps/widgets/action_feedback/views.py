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
from apps.managers.score_mgr import score_mgr
#from django.db.models.aggregates import Count


def supply(request, page_name):
    """Supply view_objects for the Action_Feedback template."""
    _ = page_name
    _ = request

    return {
        "action_feedback": feedback_analysis.get_action_likert_scales(),
        "analysis": feedback_analysis.get_analysis(),
        "stacked": feedback_analysis.build_feedback_data(),
        "google": feedback_analysis.build_google_chart_data()
    }


@never_cache
@login_required
def action_feedback(request, action_type, slug):
    """Handle feedback for an action."""
    _ = action_type
    action = smartgrid.get_action(slug=slug)
    user = request.user
    profile = request.user.get_profile()

    form = ActionFeedbackForm(request.POST)
    if form.is_valid():
        print form.cleaned_data
    feedback, created = ActionFeedback.objects.get_or_create(action=action, user=user)

    if 'Score' in request.POST:
        feedback.rating = request.POST['Score']
    else:
        feedback.rating = 0
    if 'comments' in request.POST:
        feedback.comment = request.POST['comments']
    else:
        feedback.comment = ""
    feedback.changed = datetime.datetime.now()
    feedback.save()

    if created:
        # Give the user points for providing feedback
        profile.add_points(score_mgr.feedback_points(),
                           datetime.datetime.today(),
                           "%s provided feedback about %s" % (user.username, action.name))
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
        "scale": feedback_analysis.get_likert_scale_totals(action),
        }, context_instance=RequestContext(request))


@never_cache
@login_required
def change_feedback(request, action_type, slug):
    """Allows the user to change their feedback for an action."""
    _ = action_type
    action = smartgrid.get_action(slug)
    user = request.user
    feedback = ActionFeedback.objects.get(action=action.pk, user=user.pk)

    return render_to_response("change_feedback.html", {
        "action": action,
        "feedback": feedback,
        "user": user
        }, context_instance=RequestContext(request))
