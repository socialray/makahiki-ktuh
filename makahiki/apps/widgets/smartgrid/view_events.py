"""handles rendering events."""

import simplejson as json

from django.db import  IntegrityError
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from apps.managers.player_mgr import player_mgr
from apps.managers.score_mgr import score_mgr

from apps.widgets.smartgrid.models import  ActionMember, \
    Action, Event, ConfirmationCode
from apps.widgets.smartgrid.forms import EventCodeForm, ActivityCodeForm


def view(request, action):
    """Returns the activity info"""

    social_email = None
    social_email2 = None
    if action.member:
        social_email = action.member.social_email
        social_email2 = action.member.social_email2

    form = ActivityCodeForm(
            initial={"social_email": social_email, "social_email2": social_email2},
            request=request)

    form.form_title = "Sign up for this event"

    return form


def add(request, event):
    """Handle the Submission and claim point of the event."""
    if event.is_event_completed():
        return complete(request, event)
    else:
        return signup(request, event)


def signup(request, event):
    """Commit the current user to the activity."""
    user = request.user
    value = None

    # Search for an existing activity for this user
    if event not in user.action_set.all():
        action_member = ActionMember(user=user, action=event)
        action_member.save()

        response = HttpResponseRedirect(
            reverse("activity_task", args=(event.type, event.slug,)))
        value = score_mgr.signup_points()
        notification = "You just earned " + str(value) + " points."
        response.set_cookie("task_notify", notification)
        return response

    # adding to the existing activity results in redirecting to the task page
    return HttpResponseRedirect(reverse("activity_task", args=(event.type, event.slug,)))


def complete(request, event):
    """complete the event and try to claim point."""

    user = request.user

    if request.method == "POST":
        form = ActivityCodeForm(request.POST, request=request, action=event)

        if form.is_valid():
            # Approve the activity (confirmation code is validated in
            # forms.ActivityTextForm.clean())
            code = ConfirmationCode.objects.get(code=form.cleaned_data["response"])
            code.is_active = False
            code.save()

            try:
                action_member = ActionMember.objects.get(user=user, action=event)
            except ObjectDoesNotExist:
                action_member = ActionMember(user=user, action=event)

            action_member.approval_status = "approved"
            value = event.point_value

            action_member.social_email = form.cleaned_data["social_email"]
            try:
                action_member.save()
            except IntegrityError:
                messages.error = 'Sorry, but it appears that you have already added this activity.'
                return HttpResponseRedirect(
                    reverse("activity_task", args=(event.type, event.slug,)))

            response = HttpResponseRedirect(
                reverse("activity_task", args=(event.type, event.slug,)))
            if value:
                notification = "You just earned " + str(value) + " points."
                response.set_cookie("task_notify", notification)

            return response

        # invalid form
        return render_to_response("task.html", {
            "action": event,
            "form": form,
            "completed_count": 0,
            "team_members": None,
            "display_form": True,
            "reminders": None,
            }, context_instance=RequestContext(request))

    return HttpResponseRedirect(reverse("activity_task", args=(event.type, event.slug,)))


@never_cache
@login_required
def view_codes(request, action_type, slug):
    """View the confirmation codes for a given activity."""
    _ = action_type
    if not request.user or not request.user.is_staff:
        raise Http404

    per_page = 10
    # Check for a rows parameter
    if "rows" in request.GET:
        per_page = int(request.GET['rows'])

    event = get_object_or_404(Event, slug=slug)
    codes = ConfirmationCode.objects.filter(action=event)
    if len(codes) == 0:
        raise Http404

    return render_to_response("view_codes.html", {
        "activity": event,
        "codes": codes,
        "per_page": per_page,
        }, context_instance=RequestContext(request))


@never_cache
@login_required
def view_rsvps(request, action_type, slug):
    """View the RSVP list"""
    _ = action_type
    if not request.user or not request.user.is_staff:
        raise Http404

    action = get_object_or_404(Action, slug=slug)
    rsvps = ActionMember.objects.filter(
        action=action,
        approval_status='pending'
    ).order_by('user__last_name', 'user__first_name')

    return render_to_response("rsvps.html", {
        "activity": action,
        "rsvps": rsvps,
        }, context_instance=RequestContext(request))


def _check_attend_code(user, form):
    """Check the confirmation code in AJAX."""
    social_email = None
    code = None
    message = None

    try:
        code = ConfirmationCode.objects.get(code=form.cleaned_data["response"].lower())
        if not code.is_active:
            message = "This code has already been used."
        elif code.action in user.action_set.filter(actionmember__award_date__isnull=False):
            message = "You have already redemmed a code for this event/excursion."
        elif code.action.social_bonus:
            if form.cleaned_data["social_email"]:
                if form.cleaned_data["social_email"] != "Email":
                    ref_user = player_mgr.get_user_by_email(form.cleaned_data["social_email"])
                    if ref_user == None or ref_user == user:
                        message = "Invalid email. Please input only one valid email."
                        social_email = "true"
                else:
                    message = "Please enter one UH email or clear the email to submit"
                    social_email = "true"

    except ConfirmationCode.DoesNotExist:
        message = "This code is not valid."
    except KeyError:
        message = "Please input code."
    return message, social_email, code


def attend_code(request):
    """Claim the attendance code"""

    user = request.user
    action_member = None
    message = None
    social_email = None

    if request.is_ajax() and request.method == "POST":
        form = EventCodeForm(request.POST)
        if form.is_valid():
            message, social_email, code = _check_attend_code(user, form)

            if message:
                return HttpResponse(json.dumps({
                    "message": message,
                    "social_email": social_email
                }), mimetype="application/json")

            try:
                action_member = ActionMember.objects.get(user=user, action=code.action)
            except ObjectDoesNotExist:
                action_member = ActionMember(user=user, action=code.action)

            action_member.approval_status = "approved"
            value = code.action.point_value

            if "social_email" in form.cleaned_data and \
               form.cleaned_data["social_email"] != "Email":
                action_member.social_email = form.cleaned_data["social_email"]

            # Model save method will award the points.
            action_member.save()

            code.is_active = False
            code.save()

            response = HttpResponse(json.dumps({
                "redirectUrl": reverse("activity_task", args=(code.action.type, code.action.slug))
            }), mimetype="application/json")
            notification = "You just earned " + str(value) + " points."
            response.set_cookie("task_notify", notification)
            return response

        # At this point there is a form validation error.
        return HttpResponse(json.dumps({
            "message": "Please input code."
        }), mimetype="application/json")

    raise Http404
