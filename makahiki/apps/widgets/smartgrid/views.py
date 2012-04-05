"""Prepares the rendering of Smart Grid Game widget."""

import datetime
from django.db.models.query_utils import Q
import simplejson as json

from django.db import  IntegrityError
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from apps.managers.cache_mgr import cache_mgr

from apps.widgets.smartgrid.models import TextPromptQuestion, EmailReminder, ActivityMember, \
                                     CommitmentMember, Category, ActivityBase, Activity, \
                                     ConfirmationCode, TextReminder, activity_image_file_path
from apps.widgets.smartgrid import can_add_commitments, can_complete_commitments, \
                              annotate_simple_task_status, is_pending_commitment, \
                              is_unlock_from_cache, get_user_by_email
from apps.widgets.smartgrid.forms import EventCodeForm, SurveyForm, CommitmentCommentForm, \
                                    ActivityCodeForm, ActivityFreeResponseForm, \
                                    ActivityImageForm, ActivityTextForm, \
                                    ActivityFreeResponseImageForm, ReminderForm


MAX_INDIVIDUAL_STANDINGS = 10
smartgrid_COL_COUNT = 3


def supply(request, page_name):
    """Supplies view_objects for smartgrid widgets."""
    _ = page_name

    user = request.user

    return {
        "categories": _get_categories(user),
        }


def _get_categories(user):
    """Return the category list with the tasks info"""
    categories = cache_mgr.get('smartgrid-categories-%s' % user.username)
    if not categories:
        activity_members = []
        for member in ActivityMember.objects.filter(user=user):
            member_dict = {}
            member_dict["activity_id"] = member.activity_id
            member_dict["slug"] = member.activity.slug
            member_dict["approval_status"] = member.approval_status
            member_dict["award_date"] = member.award_date
            activity_members.append(member_dict)

        commitment_members = []
        for member in CommitmentMember.objects.filter(user=user):
            member_dict = {}
            member_dict["commitment_id"] = member.commitment_id
            member_dict["slug"] = member.commitment.slug
            member_dict["completion_date"] = member.completion_date
            member_dict["award_date"] = member.award_date
            commitment_members.append(member_dict)

        tasks = []
        for task in ActivityBase.objects.all().order_by("category__id", "priority"):
            task_dict = {}
            task_dict["category_id"] = task.category_id
            task_dict["id"] = task.id
            task_dict["type"] = task.type
            task_dict["depends_on"] = task.depends_on
            task_dict["depends_on_text"] = task.depends_on_text
            task_dict["slug"] = task.slug
            task_dict["name"] = task.name
            if task.type == "commitment":
                task = task.commitment
                task_dict["commitment_point_value"] = task.point_value
            else:
                task = task.activity
                task_dict["event_date"] = task.event_date
                task_dict["activity_point_value"] = task.point_value
                task_dict["point_range_start"] = task.point_range_start
                task_dict["point_range_end"] = task.point_range_end
            tasks.append(task_dict)

        for task in tasks:
            annotate_simple_task_status(user, task, activity_members, commitment_members)

        categories = Category.objects.all()
        for cat in categories:
            task_list = []
            for task in tasks:
                if task["category_id"] == cat.id:
                    task_list.append(task)
            cat.task_list = task_list

        # Cache the categories for an hour (or until they are invalidated)
        cache_mgr.set('smartgrid-categories-%s' % user,
            categories, 60 * 60)

    return categories


@never_cache
@login_required
def view_codes(request, activity_type, slug):
    """View the confirmation codes for a given activity."""
    if not request.user or not request.user.is_staff:
        raise Http404

    per_page = 10
    # Check for a rows parameter
    if "rows" in request.GET:
        per_page = int(request.GET['rows'])

    activity = get_object_or_404(ActivityBase, type=activity_type, slug=slug)
    codes = ConfirmationCode.objects.filter(activity=activity)
    if len(codes) == 0:
        raise Http404

    return render_to_response("view_codes.html", {
        "activity": activity,
        "codes": codes,
        "per_page": per_page,
        }, context_instance=RequestContext(request))


@never_cache
@login_required
def view_rsvps(request, activity_type, slug):
    """View the RSVP list"""
    _ = activity_type
    if not request.user or not request.user.is_staff:
        raise Http404

    activity = get_object_or_404(Activity, slug=slug)
    rsvps = ActivityMember.objects.filter(
        activity=activity,
        approval_status='pending'
    ).order_by('user__last_name', 'user__first_name')

    return render_to_response("rsvps.html", {
        "activity": activity,
        "rsvps": rsvps,
        }, context_instance=RequestContext(request))


def _check_attend_code(user, form):
    """Check the confirmation code in AJAX."""
    try:
        code = ConfirmationCode.objects.get(code=form.cleaned_data["response"].lower())
        if not code.is_active:
            message = "This code has already been used."
        elif code.activity in user.activity_set.filter(activitymember__award_date__isnull=False):
            message = "You have already redemmed a code for this event/excursion."
        elif code.activity.social_bonus:
            if form.cleaned_data["social_email"]:
                if form.cleaned_data["social_email"] != "Email":
                    ref_user = get_user_by_email(form.cleaned_data["social_email"])
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
    activity_member = None
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
                activity_member = ActivityMember.objects.get(user=user, activity=code.activity)
            except ObjectDoesNotExist:
                activity_member = ActivityMember(user=user, activity=code.activity)

            activity_member.approval_status = "approved"
            value = code.activity.point_value

            if "social_email" in form.cleaned_data and \
               form.cleaned_data["social_email"] != "Email":
                activity_member.social_email = form.cleaned_data["social_email"]

            # Model save method will award the points.
            activity_member.save()

            code.is_active = False
            code.save()

            response = HttpResponse(json.dumps({
                "type": code.activity.type,
                "slug": code.activity.slug,
                }), mimetype="application/json")
            notification = "You just earned " + str(value) + " points."
            response.set_cookie("task_notify", notification)
            return response

        # At this point there is a form validation error.
        return HttpResponse(json.dumps({
            "message": "Please input code."
        }), mimetype="application/json")

    raise Http404


def __add_commitment(request, commitment):
    """Commit the current user to the commitment."""
    user = request.user
    value = None
    form = None

    if request.method == "POST":
        form = CommitmentCommentForm(request.POST, request=request, activity=commitment)
        if not form.is_valid():
            return render_to_response("task.html", {
                "task": commitment,
                "pau": True,
                "form": form,
                "question": None,
                "member_all": 0,
                "member_team": 0,
                "display_form": True,
                "form_title": "Get your points",
                }, context_instance=RequestContext(request))

    # now we either have a valid form or a GET
    if is_pending_commitment(user, commitment):
        if form and can_complete_commitments(user, commitment):
            try:
                member = user.commitmentmember_set.get(commitment=commitment, award_date=None)
            except ObjectDoesNotExist:
                # ignore the race condition
                return HttpResponseRedirect(
                    reverse("activity_task", args=(commitment.type, commitment.slug,)))

            #commitment end, award full point
            member.award_date = datetime.datetime.today()

            if form.cleaned_data["social_email"]:
                member.social_email = form.cleaned_data["social_email"]
            if form.cleaned_data["social_email2"]:
                member.social_email2 = form.cleaned_data["social_email2"]
            member.save()
            value = commitment.point_value
        else:   # it is a GET, redirect to task page
            return  HttpResponseRedirect(
                reverse("activity_task", args=(commitment.type, commitment.slug,)))

    elif can_add_commitments(user):
        # User can commit to this commitment. allow to commit to completed commitment again
        # as long as the pending does not reach max
        member = CommitmentMember(user=user, commitment=commitment)

        if form:
            member.social_email = form.cleaned_data["social_email"]
            member.social_email2 = form.cleaned_data["social_email2"]

        try:
            member.save()
        except IntegrityError:
            messages.error = 'Sorry, but it appears that you are already participating in ' \
                             'this commitment.'
            return HttpResponseRedirect(
                reverse("activity_task", args=(commitment.type, commitment.slug,)))

        # messages.info("You are now committed to \"%s\"" % commitment.title)

        #increase the point from signup
        message = "Commitment: %s (Sign up)" % (commitment.title)
        user.get_profile().add_points(2, datetime.datetime.today() - datetime.timedelta(minutes=1),
            message, member)
        user.get_profile().save()
        value = 2
    else:
    # user can not add more than 5 commitment
        return  HttpResponseRedirect(
            reverse("activity_task", args=(commitment.type, commitment.slug,)))

    response = HttpResponseRedirect(
        reverse("activity_task", args=(commitment.type, commitment.slug,)))
    notification = "You just earned " + str(value) + " points."
    response.set_cookie("task_notify", notification)
    return response


def __drop_commitment(request, commitment):
    """drop the commitment."""
    user = request.user

    if commitment in user.commitment_set.all():
        # User can drop this commitment.
        try:
            member = user.commitmentmember_set.get(commitment=commitment, award_date=None)

            #decrease sign up point
            message = "Commitment: %s (Drop)" % (commitment.title)
            value = 2
            user.get_profile().remove_points(value,
                datetime.datetime.today() - datetime.timedelta(minutes=1), message, member)
            user.get_profile().save()

            member.delete()

            response = HttpResponseRedirect(
                reverse("activity_task", args=(commitment.type, commitment.slug,)))
            notification = "Commitment dropped. you lose " + str(value) + " points."
            response.set_cookie("task_notify", notification)
            return response

        except ObjectDoesNotExist:
            pass

    # Fall through, the user is not participating in this commitment
    messages.error = 'It appears that you are not participating in this commitment.'
    # Take them back to the commitment page.
    return HttpResponseRedirect(reverse("activity_task", args=(commitment.type, commitment.slug,)))


def __add_activity(request, activity):
    """Commit the current user to the activity."""
    user = request.user
    value = None

    # Search for an existing activity for this user
    if activity not in user.activity_set.all():
        if activity.type == 'survey':
            question = TextPromptQuestion.objects.filter(activity=activity)
            form = SurveyForm(request.POST or None, questions=question)

            if form.is_valid():
                for i, q in enumerate(question):
                    activity_member = ActivityMember(user=user, activity=activity)
                    activity_member.question = q
                    activity_member.response = form.cleaned_data['choice_response_%s' % i]

                    if i == (len(question) - 1):
                        activity_member.approval_status = "approved"

                    try:
                        activity_member.save()
                    except IntegrityError:
                        messages.error = 'Sorry, but it appears that you have already added ' \
                                         'this activity.'
                        return HttpResponseRedirect(
                            reverse("activity_task", args=(activity.type, activity.slug,)))

                    value = activity.point_value

            else:   # form not valid
                return render_to_response("task.html", {
                    "task": activity,
                    "pau": False,
                    "form": form,
                    "question": question,
                    "display_form": True,
                    "form_title": "Survey",
                    }, context_instance=RequestContext(request))

        else:  # other than survey
            activity_member = ActivityMember(user=user, activity=activity)
            activity_member.save()

            #increase point
            message = "%s: %s (Sign up)" % (activity.type.capitalize(), activity.title)
            user.get_profile().add_points(
                2,
                datetime.datetime.today() - datetime.timedelta(minutes=1),
                message,
                activity_member)
            user.get_profile().save()
            value = 2

        response = HttpResponseRedirect(
            reverse("activity_task", args=(activity.type, activity.slug,)))
        notification = "You just earned " + str(value) + " points."
        response.set_cookie("task_notify", notification)
        return response

    # adding to the existing activity results in redirecting to the task page
    return HttpResponseRedirect(reverse("activity_task", args=(activity.type, activity.slug,)))


def __drop_activity(request, activity):
    """Drop the current user from the activity."""
    user = request.user

    # Search for an existing activity for this user
    if activity in user.activity_set.all():
        try:
            activity_member = user.activitymember_set.get(activity=activity)

            #decrease point
            message = "%s: %s (Drop)" % (activity.type.capitalize(), activity.title)
            user.get_profile().remove_points(
                2,
                datetime.datetime.today() - datetime.timedelta(minutes=1),
                message,
                activity_member)
            user.get_profile().save()
            value = 2

            activity_member.delete()

            response = HttpResponseRedirect(
                reverse("activity_task", args=(activity.type, activity.slug,)))
            notification = "Removed from signup list. you lose " + str(value) + " points."
            response.set_cookie("task_notify", notification)
            return response

        except ObjectDoesNotExist:
            pass

    # Fall through.
    # If they are already not participating, then they should be taken to the task page.
    messages.error = 'It appears that you are not participating in this activity.'
    return HttpResponseRedirect(reverse("activity_task", args=(activity.type, activity.slug,)))


def _get_form(request, activity):
    """Returns the activity form."""

    if activity.confirm_type == "image":
        form = ActivityImageForm(request.POST, request.FILES, request=request, activity=activity)
    elif activity.confirm_type == "free":
        form = ActivityFreeResponseForm(request.POST, request=request, activity=activity)
    elif activity.confirm_type == "free_image":
        form = ActivityFreeResponseImageForm(request.POST, request.FILES, request=request,
                                             activity=activity)
    elif activity.confirm_type == "code":
        form = ActivityCodeForm(request.POST, request=request, activity=activity)
    else:
        form = ActivityTextForm(request.POST, request=request, activity=activity)
    return form


def __request_activity_points(request, activity):
    """Creates a request for points for an activity."""

    user = request.user
    question = None
    activity_member = None
    value = None

    try:
        # Retrieve an existing activity member object if it exists.
        activity_member = ActivityMember.objects.get(user=user, activity=activity)
    except ObjectDoesNotExist:
        pass

    if request.method == "POST":
        form = _get_form(request, activity)

        ## print activity.confirm_type
        if form.is_valid():
            if not activity_member:
                activity_member = ActivityMember(user=user, activity=activity)

            # Attach image if it is an image form.
            if "image_response" in form.cleaned_data:
                if activity.confirm_type == "free_image":
                    activity_member.response = form.cleaned_data["response"]

                path = activity_image_file_path(user=user,
                    filename=request.FILES['image_response'].name)
                activity_member.image = path
                activity_member.image.storage.save(path, request.FILES["image_response"])
                activity_member.approval_status = "pending"

            elif activity.confirm_type == "code":
                # Approve the activity (confirmation code is validated in
                # forms.ActivityTextForm.clean())
                code = ConfirmationCode.objects.get(code=form.cleaned_data["response"])
                code.is_active = False
                code.save()
                activity_member.approval_status = "approved"
                value = activity.point_value

            # Attach text prompt question if one is provided
            elif "question" in form.cleaned_data:
                activity_member.question = TextPromptQuestion.objects.get(
                    pk=form.cleaned_data["question"])
                activity_member.response = form.cleaned_data["response"]
                activity_member.approval_status = "pending"

            elif activity.confirm_type == "free":
                activity_member.response = form.cleaned_data["response"]
                activity_member.approval_status = "pending"

            activity_member.social_email = form.cleaned_data["social_email"]
            try:
                activity_member.save()
            except IntegrityError:
                messages.error = 'Sorry, but it appears that you have already added this activity.'
                return HttpResponseRedirect(
                    reverse("activity_task", args=(activity.type, activity.slug,)))

            response = HttpResponseRedirect(
                reverse("activity_task", args=(activity.type, activity.slug,)))
            if value:
                notification = "You just earned " + str(value) + " points."
                response.set_cookie("task_notify", notification)

            return response

        # if invalid form
        if activity.confirm_type == "text":
            question = activity.pick_question(user.id)

        return render_to_response("task.html", {
            "task": activity,
            "pau": False,
            "form": form,
            "question": question,
            "member_all": 0,
            "member_team": 0,
            "display_form": True,
            "form_title": "Get your points",
            }, context_instance=RequestContext(request))

        # if not POST, return to task page
    return HttpResponseRedirect(reverse("activity_task", args=(activity.type, activity.slug,)))


def _load_reminders(task, user, member_all_count):
    """Load the reminders."""
    reminders = {}
    if task.type == "event" or task.type == "excursion":
        task.available_seat = task.event_max_seat - member_all_count
        # Store initial reminder fields.
        reminder_init = {"email": user.get_profile().contact_email or user.email,
            "text_number": user.get_profile().contact_text,
            "text_carrier": user.get_profile().contact_carrier}
        # Retrieve an existing reminder and update it accordingly.
        try:
            email = user.emailreminder_set.get(activity=task)
            reminders.update({"email": email})
            reminder_init.update({
                "email": email.email_address,
                "send_email": True,
                "email_advance": str((task.activity.event_date - email.send_at).seconds / 3600)})
        except ObjectDoesNotExist:
            pass
        try:
            text = user.textreminder_set.get(activity=task)
            reminders.update({"text": text})
            reminder_init.update({
                "text_number": text.text_number,
                "text_carrier": text.text_carrier,
                "send_text": True,
                "text_advance": str((task.activity.event_date - text.send_at).seconds / 3600)})
        except ObjectDoesNotExist:
            pass

        reminders.update({"form": ReminderForm(initial=reminder_init)})
    return reminders


def _calculate_task_duration(task):
    """Calculate the task duration."""
    hours = task.duration / 60
    minutes = task.duration % 60
    task.duration = ""
    if hours > 1:
        task.duration = "%d hours" % (hours)
    elif hours > 0:
        task.duration = "%d hour" % (hours)
    if minutes > 0:
        task.duration = task.duration + " %d minutes" % (minutes)


def _create_activity_request_form(request, task, user, approval, pau):
    """ Create activity request form """
    form_title = "Get your points"

    social_email = None
    social_email2 = None

    if approval:
        social_email = approval.social_email
        social_email2 = approval.social_email2

    if task.confirm_type == "image":
        form = ActivityImageForm(
            initial={"social_email": social_email, "social_email2": social_email2},
            request=request)
    elif task.confirm_type == "text":
        question = task.pick_question(user.id)
        if question:
            form = ActivityTextForm(
                initial={"question": question.pk,
                         "social_email": social_email,
                         "social_email2": social_email2},
                question_id=question.pk,
                request=request)
    elif task.confirm_type == "free":
        form = ActivityFreeResponseForm(
            initial={"social_email": social_email, "social_email2": social_email2},
            request=request)
    elif task.confirm_type == "free_image":
        form = ActivityFreeResponseImageForm(
            initial={"social_email": social_email, "social_email2": social_email2},
            request=request)
    else:
        form = ActivityCodeForm(
            initial={"social_email": social_email, "social_email2": social_email2},
            request=request)
    if task.type == "event" or task.type == "excursion":
        if not pau:
            form_title = "Sign up for this " + task.type

    return form, form_title, question


def _view_activity(request, task, user):
    """Returns the activity info"""

    task = task.activity

    _calculate_task_duration(task)

    pau = False
    approval = None
    if task.type == "survey":
        member_all = ActivityMember.objects.exclude(user=user).filter(activity=task,
            approval_status="approved")

        question = TextPromptQuestion.objects.filter(activity=task)
        form = SurveyForm(questions=question)
        form_title = "Survey"
    else:
        member_all = ActivityMember.objects.filter(activity=task)
        members = ActivityMember.objects.filter(user=user, activity=task)
        count = members.count()

        if count == 0 and task.is_group:
            members = ActivityMember.objects.filter(
                Q(social_email=user.email) | Q(social_email2=user.email), activity=task)
            count = members.count()

        if count > 0:
            pau = True
            approval = members[0]
            if not task.has_variable_points:
                approval.points_awarded = task.point_value

        form, form_title, question = _create_activity_request_form(request, task, user,
                                                                   approval, pau)
    return task, member_all, pau, approval, form, form_title, question


def _view_commitment(request, task, user):
    """Returns commitment info."""
    task = task.commitment
    social_email = None
    social_email2 = None
    pau = False
    approval = None
    members = CommitmentMember.objects.filter(user=user, commitment=task).order_by("-updated_at")
    if members.count() > 0:
        pau = True
        approval = members[0]
        social_email = approval.social_email
        social_email2 = approval.social_email2
        approval.points_awarded = task.point_value
    member_all = CommitmentMember.objects.filter(commitment=task)
    form_title = "Make this commitment"
    form = CommitmentCommentForm(
        initial={"social_email": social_email, "social_email2": social_email2},
        request=request)
    can_commit = can_add_commitments(user) and not is_pending_commitment(user, task)
    return task, member_all, pau, approval, form, form_title, can_commit


@never_cache
@login_required
def view_task(request, activity_type, slug):
    """individual task page"""
    task = get_object_or_404(ActivityBase, type=activity_type, slug=slug)

    user = request.user

    team = user.get_profile().team
    pau = False
    question = None
    form = None
    approval = None
    can_commit = None

    if is_unlock_from_cache(user, task) != True:
        return HttpResponseRedirect(reverse("learn_index", args=()))

    if task.type != "commitment":
        task, member_all, pau, approval, form, form_title, question = _view_activity(
            request, task, user)
    else:
        task, member_all, pau, approval, form, form_title, can_commit = _view_commitment(
            request, task, user)

    reminders = _load_reminders(task, user, member_all.count())

    display_form = True if "display_form" in request.GET else False

    return render_to_response("task.html", {
        "task": task,
        "pau": pau,
        "approval": approval,
        "form": form,
        "question": question,
        "member_all": member_all.count(),
        "team_members": member_all.select_related('user__profile').filter(user__profile__team=team),
        "display_form": display_form,
        "form_title": form_title,
        "can_commit": can_commit,
        "reminders": reminders,
        }, context_instance=RequestContext(request))


@never_cache
@login_required
def add_task(request, activity_type, slug):
    """Handle the Submission of the task."""

    task = get_object_or_404(ActivityBase, type=activity_type, slug=slug)

    if task.type == "commitment":
        return __add_commitment(request, task.commitment)

    if task.type == "activity":
        return __request_activity_points(request, task.activity)
    elif task.type == "survey":
        return __add_activity(request, task)
    else:       # event or excursion
        task = task.activity
        if task.is_event_completed():
            return __request_activity_points(request, task)
        else:
            return __add_activity(request, task)


@login_required
def reminder(request, activity_type, slug):
    """Handle the send reminder request."""

    if request.is_ajax():
        if request.method == "POST":
            profile = request.user.get_profile()
            task = get_object_or_404(ActivityBase, type=activity_type, slug=slug)
            form = ReminderForm(request.POST)
            if form.is_valid():
                email_reminder = None
                text_reminder = None

                # Try and retrieve the reminders.
                try:
                    email_reminder = EmailReminder.objects.get(user=request.user, activity=task)
                    if form.cleaned_data["send_email"]:
                        email_reminder.email_address = form.cleaned_data["email"]
                        email_reminder.send_at = task.activity.event_date - datetime.timedelta(
                            hours=int(form.cleaned_data["email_advance"])
                        )
                        email_reminder.save()

                        profile.contact_email = form.cleaned_data["email"]
                        profile.save()
                    else:
                        # If send_email is false, the user does not want the reminder anymore.
                        email_reminder.delete()

                except EmailReminder.DoesNotExist:
                    # Create a email reminder
                    if form.cleaned_data["send_email"]:
                        email_reminder = EmailReminder.objects.create(
                            user=request.user,
                            activity=task,
                            email_address=form.cleaned_data["email"],
                            send_at=task.activity.event_date - datetime.timedelta(
                                hours=int(form.cleaned_data["email_advance"])
                            )
                        )

                        profile.contact_email = form.cleaned_data["email"]
                        profile.save()

                try:
                    text_reminder = TextReminder.objects.get(user=request.user, activity=task)
                    if form.cleaned_data["send_text"]:
                        text_reminder.text_number = form.cleaned_data["text_number"]
                        text_reminder.text_carrier = form.cleaned_data["text_carrier"]
                        text_reminder.send_at = task.activity.event_date - datetime.timedelta(
                            hours=int(form.cleaned_data["text_advance"])
                        )
                        text_reminder.save()

                        profile.contact_text = form.cleaned_data["text_number"]
                        profile.contact_carrier = form.cleaned_data["text_carrier"]
                        profile.save()

                    else:
                        text_reminder.delete()

                except TextReminder.DoesNotExist:
                    if form.cleaned_data["send_text"]:
                        text_reminder = TextReminder.objects.create(
                            user=request.user,
                            activity=task,
                            text_number=form.cleaned_data["text_number"],
                            text_carrier=form.cleaned_data["text_carrier"],
                            send_at=task.activity.event_date - datetime.timedelta(
                                hours=int(form.cleaned_data["text_advance"])
                            ),
                        )

                        profile.contact_text = form.cleaned_data["text_number"]
                        profile.contact_carrier = form.cleaned_data["text_carrier"]
                        profile.save()

                return HttpResponse(json.dumps({"success": True}), mimetype="application/json")

            template = render_to_string("reminder_form.html", {
                "reminders": {"form": form},
                "task": task,
                })

            return HttpResponse(json.dumps({
                "success": False,
                "form": template,
                }), mimetype="application/json")
    raise Http404


@never_cache
@login_required
def drop_task(request, activity_type, slug):
    """Handle the drop task request."""

    task = get_object_or_404(ActivityBase, type=activity_type, slug=slug)

    if task.type == "commitment":
        return __drop_commitment(request, task.commitment)

    if task.type == "event" or task.type == "excursion":
        return __drop_activity(request, task.activity)
