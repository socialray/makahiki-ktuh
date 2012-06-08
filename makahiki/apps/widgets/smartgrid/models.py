"""Smart Grid Game model definition."""

import datetime
import random

from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.localflavor.us.models import PhoneNumberField
import os

from apps.managers.score_mgr import score_mgr
from apps.managers.score_mgr.models import PointsTransaction
from apps.managers.team_mgr.models import Post
from apps.utils.utils import media_file_path
from apps.widgets.notifications.models import UserNotification
from apps.managers.cache_mgr import cache_mgr
from apps.widgets.smartgrid import NOSHOW_PENALTY_DAYS

_MEDIA_LOCATION_ACTION = os.path.join("smartgrid", "actions")
"""location for the uploaded files for actions."""

_MEDIA_LOCATION_MEMBER = os.path.join("smartgrid", "members")
"""location for the uploaded files for actionmembers."""


def activity_image_file_path(instance=None, filename=None, user=None):
    """Returns the file path used to save an activity confirmation image."""
    if instance:
        user = user or instance.user
    return os.path.join(settings.MAKAHIKI_MEDIA_PREFIX, _MEDIA_LOCATION_MEMBER,
                        user.username, filename)


class Category(models.Model):
    """Categories used to group commitments and activities."""
    name = models.CharField(max_length=255,
                            help_text="The name of the category (max 255 characters).")
    slug = models.SlugField(help_text="Automatically generated if left blank.",
                            null=True)

    class Meta:
        """Meta"""
        verbose_name_plural = "categories"

    def __unicode__(self):
        return self.name


class TextPromptQuestion(models.Model):
    """Represents questions that can be asked of users in order to verify participation
    in activities."""

    action = models.ForeignKey("Action")
    question = models.TextField(help_text="The question text.")
    answer = models.CharField(max_length=255,
                              help_text="The answer of question (max 255 characters).",
                              null=True, blank=True)

    def __unicode__(self):
        return "Question: '%s' Answer: '%s'" % (self.question, self.answer)


class QuestionChoice(models.Model):
    """Represents questions's multiple choice"""

    question = models.ForeignKey("TextPromptQuestion")
    action = models.ForeignKey("Action")
    choice = models.CharField(max_length=255,
                              help_text="The choice of question (max 255 characters).")

    def __unicode__(self):
        return self.choice


class ConfirmationCode(models.Model):
    """Represents confirmation codes for activities."""
    action = models.ForeignKey("Action")
    code = models.CharField(max_length=50, unique=True, db_index=True,
                            help_text="The confirmation code.")
    is_active = models.BooleanField(default=True, editable=False,
                                    help_text="Is the confirmation code still active?")

    @staticmethod
    def generate_codes_for_activity(event, num_codes):
        """Generates a set of random codes for the activity."""
        values = 'abcdefghijkmnpqrstuvwxyz234789'

        # Use the first non-dash component of the slug.
        components = event.slug.split('-')
        header = components[0]
        # Need to see if there are other codes with this header.
        index = 1
        while ConfirmationCode.objects.filter(code__istartswith=header).exclude(
            action=event).count() > 0 and index < len(components):
            header += components[index]
            index += 1

        header += "-"
        for _ in range(0, num_codes):
            code = ConfirmationCode(action=event, code=header)
            valid = False
            while not valid:
                for value in random.sample(values, 5):
                    code.code += value
                try:
                    # print code.code
                    # Throws exception if the code is a duplicate.
                    code.save()
                    valid = True
                except IntegrityError:
                    # Try again.
                    code.code = header


class Action(models.Model):
    """Activity Base class."""
    TYPE_CHOICES = (
        ('activity', 'Activity'),
        ('commitment', 'Commitment'),
        ('event', 'Event'),
        ('excursion', 'Excursion'),
        )

    RESOURCE_CHOICES = (
        ('energy', 'Energy'),
        ('water', 'Water'),
        ('waste', 'Waste'),
    )

    VIDEO_SOURCE_CHOICES = (
        ('youtube', 'youtube'),
    )

    users = models.ManyToManyField(User, through="ActionMember")

    name = models.CharField(
        max_length=20,
        help_text="The name of the action.")
    slug = models.SlugField(
        help_text="Automatically generated if left blank.",
        )
    title = models.CharField(
        max_length=200,
        help_text="The title of the action.")
    image = models.ImageField(
        max_length=255, blank=True, null=True,
        upload_to=media_file_path(_MEDIA_LOCATION_ACTION),
        help_text="Uploaded image for the activity.")
    video_id = models.CharField(
        null=True, blank=True,
        max_length=200,
        help_text="The id of the video.")
    video_source = models.CharField(
        null=True, blank=True,
        max_length=20,
        choices=VIDEO_SOURCE_CHOICES,
        help_text="The source of the video.")
    embedded_widget = models.CharField(
        null=True, blank=True,
        max_length=50,
        help_text="The name of the embedded widget.")
    description = models.TextField(
        help_text=settings.MARKDOWN_TEXT)
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        help_text="The type of the actions."
    )
    level = models.IntegerField(
        default=1,
        help_text="The level of the action.")
    category = models.ForeignKey(Category,
        null=True, blank=True,
        help_text="The category of the action.")
    priority = models.IntegerField(
        default=1000,
        help_text="Activities with lower values (higher priority) will be listed first."
    )
    pub_date = models.DateField(
        default=datetime.date.today(),
        verbose_name="Publication date",
        help_text="Date at which the action will be available for users."
    )
    expire_date = models.DateField(
        null=True, blank=True,
        verbose_name="Expiration date",
        help_text="Date at which the action will be removed."
    )
    depends_on = models.CharField(
        max_length=400, null=True, blank=True,
        help_text="The condition that the unlocking of this action depends on.")
    depends_on_text = models.CharField(
        max_length=400, null=True, blank=True,
        help_text="The description of the depends on condition.")
    related_resource = models.CharField(
        max_length=20,
        null=True, blank=True,
        choices=RESOURCE_CHOICES,
        help_text="The resource this action related.")
    social_bonus = models.IntegerField(
        default=0,
        help_text="Social bonus points.")
    is_canopy = models.BooleanField(
        default=False,
        verbose_name="Canopy Activity",
        help_text="Check this box if this is a canopy activity."
    )
    is_group = models.BooleanField(default=False,
        verbose_name="Group Activity",
        help_text="Check this box if this is a group activity."
    )
    point_value = models.IntegerField(
        default=0,
        help_text="The point value to be awarded."
    )

    def __unicode__(self):
        return "%s: %s" % (self.type.capitalize(), self.title)

    def get_action(self, action_type):
        """Returns the concrete action object by type."""
        return action_type.objects.get(action_ptr=self.pk)


class Commitment(Action):
    """Commitments involve non-verifiable actions that a user can commit to.
    Typically, they will be worth fewer points than activities."""
    duration = models.IntegerField(
        default=5,
        help_text="Duration of commitment, in days."
    )

    def save(self, *args, **kwargs):
        """Custom save method to set fields."""
        self.type = "commitment"
        super(Commitment, self).save(args, kwargs)


class Activity(Action):
    """Activities involve verifiable actions that users commit to.  These actions can be
   verified by asking questions or posting an image attachment that verifies the user did
   the activity."""

    class Meta:
        """meta"""
        verbose_name_plural = "activities"

    CONFIRM_CHOICES = (
        ('text', 'Question and Answer'),
        ('image', 'Image Upload'),
        ('free', 'Free Response'),
        ('free_image', 'Free Response and Image Upload'),
        )

    duration = models.IntegerField(
        verbose_name="Expected activity duration",
        help_text="Time (in minutes) that the activity is expected to take."
    )
    point_range_start = models.IntegerField(
        null=True,
        blank=True,
        help_text="Minimum number of points possible for this activity."
    )
    point_range_end = models.IntegerField(
        null=True,
        blank=True,
        help_text="Maximum number of points possible for this activity."
    )
    confirm_type = models.CharField(
        max_length=20,
        choices=CONFIRM_CHOICES,
        default="text",
        verbose_name="Confirmation Type"
    )
    confirm_prompt = models.TextField(
        blank=True,
        verbose_name="Confirmation prompt",
        help_text="Text to display to user when asking for response."
    )

    def is_active(self):
        """Determines if the activity is available for users to participate."""
        return self.is_active_for_date(datetime.date.today())

    def is_active_for_date(self, date):
        """Determines if the activity is available for user participation at the given date."""
        pub_result = date - self.pub_date
        expire_result = self.expire_date - date
        if pub_result.days < 0 or expire_result.days < 0:
            return False
        return True

    def pick_question(self, user_id):
        """Choose a random question to present to a user."""
        if self.confirm_type != "text":
            return None

        questions = TextPromptQuestion.objects.filter(action=self)
        if questions:
            return questions[user_id % len(questions)]
        else:
            return None


class Event(Action):
    """Events will be verified by confirmation code. It includes events and excursions."""

    duration = models.IntegerField(
        verbose_name="Expected activity duration",
        help_text="Time (in minutes) that the activity is expected to take."
    )
    event_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date and time of the event",
        help_text="Required for events."
    )
    event_location = models.CharField(
        blank=True,
        null=True,
        max_length=200,
        verbose_name="Event Location",
        help_text="Location of the event"
    )
    event_max_seat = models.IntegerField(
        default=1000,
        help_text="Specify the max number of seats available to the event."
    )

    def is_event_completed(self):
        """Determines if the event is completed."""
        result = datetime.datetime.today() - self.event_date
        if result.days >= 0 and result.seconds >= 0:
            return True
        return False


class ActionMember(models.Model):
    """Represents the join between commitments and users.  Has fields for
    commenting on a commitment and whether or not the commitment is currently
    active."""

    STATUS_TYPES = (
        ('pending', 'Pending approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        )

    user = models.ForeignKey(User)
    action = models.ForeignKey(Action)
    question = models.ForeignKey(TextPromptQuestion, null=True, blank=True)
    notifications = generic.GenericRelation(UserNotification, editable=False)
    pointstransactions = generic.GenericRelation(PointsTransaction, editable=False)

    submission_date = models.DateTimeField(
        editable=False,
        help_text="The submission date.")
    completion_date = models.DateField(
        null=True, blank=True,
        help_text="The completion date."
    )
    award_date = models.DateTimeField(
        null=True, blank=True, editable=False,
        help_text="The award date.")
    approval_status = models.CharField(
        max_length=20, choices=STATUS_TYPES, default="pending",
        help_text="The approval status.")
    social_bonus_awarded = models.BooleanField(default=False,
        help_text="Is the social bonus awarded?")
    comment = models.TextField(
        blank=True,
        help_text="The comment from user submission.")
    social_email = models.TextField(
        blank=True, null=True,
        help_text="Email address of the person the user went with.")
    social_email2 = models.TextField(
        blank=True, null=True,
        help_text="Email address of the person the user went with.")
    response = models.TextField(
        blank=True,
        help_text="The response of the submission.")
    admin_comment = models.TextField(
        blank=True,
        help_text="Reason for approval/rejection")
    image = models.ImageField(
        max_length=1024, blank=True,
        upload_to=activity_image_file_path,
        help_text="Uploaded image for verification.")
    points_awarded = models.IntegerField(
        blank=True, null=True,
        help_text="Number of points to award for activities with variable point values.")

    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(editable=False, auto_now=True, null=True)

    class Meta:
        """meta"""
        unique_together = ('user', 'action', 'submission_date')

    def __unicode__(self):
        return "%s : %s" % (self.action.title, self.user.username)

    def active(self):
        """return active member"""
        return self.approval_status == "approved"

    def days_left(self):
        """
        Returns how many days are left before the user can submit the activity.
        """
        diff = self.completion_date - datetime.date.today()
        if diff.days < 0:
            return 0

        return diff.days

    def save(self, *args, **kwargs):
        """custom save method."""

        if self.social_bonus_awarded:
            # only awarding social bonus
            super(ActionMember, self).save(args, kwargs)
            return

        if not self.points_awarded:
            self.points_awarded = self.action.point_value

        if self.approval_status == u"rejected":
            self.award_date = None
            super(ActionMember, self).save(args, kwargs)

            self._handle_activity_rejected()
        else:
            # Check for any notifications and mark them as read.
            self.notifications.update(unread=False)

            # Check for admin message and generate notification
            if self.admin_comment:
                # Construct the message to be sent.
                message = "An admin made the following comment about your submission to "
                message += "<a href='%s'>%s</a> %s:" % (
                    reverse("activity_task", args=(self.action.type, self.action.slug,)),
                    self.action.title,
                    # The below is to tell the javascript to convert into a pretty date.
                    # See the prettyDate function in media/js/makahiki.js
                    "<span class='rejection-date' title='%s'></span>"
                    % self.submission_date.isoformat(),
                ) + "</br></br>" + self.admin_comment

                UserNotification.create_info_notification(
                    self.user,
                    message,
                    True,
                    content_object=self
                )

            if self.approval_status == u"pending":
                # Mark pending items as submitted.

                self.submission_date = datetime.datetime.today()

                if self.action.type == "commitment" and not self.completion_date:
                    self.completion_date = self.submission_date + \
                        datetime.timedelta(days=self.action.commitment.duration)

                super(ActionMember, self).save(args, kwargs)

                self._award_signup_points()

            else:    # is approved
                # Record dates.
                self.award_date = datetime.datetime.today()

                if self.submission_date:
                    if self.action.type == "event":
                        # this is an event with signup
                        # must save before awarding point due to the generic foreign key relation
                        super(ActionMember, self).save(args, kwargs)
                        self._award_possible_reverse_penalty_points()
                else:
                    # always make sure the submission_date is set
                    self.submission_date = self.award_date

                # must save before awarding point due to the generic foreign key relation
                super(ActionMember, self).save(args, kwargs)
                self._award_points()

                self.social_bonus_awarded = self._award_possible_social_bonus()
                if self.social_bonus_awarded:
                    super(ActionMember, self).save(args, kwargs)

                # generate notification if feedback is present
        self.post_to_wall()
        self.invalidate_cache()

    def _award_points(self):
        """Custom save method to award points."""
        profile = self.user.get_profile()

        points = self.action.point_value
        if not points:
            points = self.points_awarded

        if self.action.type == "activity":
            transaction_date = self.submission_date
        elif self.action.type == "commitment":
            transaction_date = self.award_date
        else:  # is Event
            transaction_date = self.award_date

        profile.add_points(points, transaction_date, self.action, self)

    def _award_possible_social_bonus(self):
        """award possible social bonus."""

        profile = self.user.get_profile()
        social_message = "%s (Social Bonus)" % self.action

        # award social bonus to others who referenced my email and successfully completed
        # the activity
        ref_members = ActionMember.objects.filter(action=self.action,
                                                  approval_status="approved",
                                                  social_email=self.user.email)
        for m in ref_members:
            if not m.social_bonus_awarded:
                ref_profile = m.user.get_profile()
                ref_profile.add_points(m.action.social_bonus,
                                       m.award_date,
                                       social_message, self)
                m.social_bonus_awarded = True
                m.save()

        ## award social bonus to myself if the ref user had successfully completed the activity
        if self.social_email and not self.social_bonus_awarded:
            ref_members = ActionMember.objects.filter(social_email=self.social_email,
                                                      approval_status="approved",
                                                      action=self.action)
            for m in ref_members:
                profile.add_points(self.action.social_bonus,
                                   self.award_date,
                                   social_message, self)
                return True

        return False

    def _award_signup_points(self):
        """award the sign up point for commitment and event."""

        if self.action.type != "activity":
            #increase the point from signup
            message = "%s (Sign up)" % self.action
            self.user.get_profile().add_points(score_mgr.signup_points(),
                                               self.submission_date,
                                               message,
                                               self)

    def _drop_signup_points(self):
        """award the sign up point for commitment and event."""

        if self.action.type != "activity":
            #increase the point from signup
            message = "%s (Drop Sign up)" % self.action
            self.user.get_profile().remove_points(score_mgr.signup_points(),
                                               self.submission_date,
                                               message,
                                               self)

    def _award_possible_reverse_penalty_points(self):
        """ reverse event/excursion noshow penalty."""
        if self._has_noshow_penalty():
            message = "%s (Reverse No Show Penalty)" % self.action
            self.user.get_profile().add_points(score_mgr.noshow_penalty_points(),
                               self.award_date,
                               message,
                               self)

    def _has_noshow_penalty(self):
        """if NOSHOW_PENALTY_DAYS past and has submission_date (signed up),
        return true as noshow penalty."""
        event = self.action.event
        diff = datetime.date.today() - event.event_date.date()
        if diff.days > NOSHOW_PENALTY_DAYS and self.submission_date:
            return True
        else:
            return False

    def _handle_activity_rejected(self):
        """Creates a notification for rejected tasks.  This also creates an email message if
        it is configured.
        """
        # Construct the message to be sent.
        message = "Your response to <a href='%s'>%s</a> %s was not approved." % (
            reverse("activity_task", args=(self.action.type, self.action.slug,)),
            self.action.title,
            # The below is to tell the javascript to convert into a pretty date.
            # See the prettyDate function in media/js/makahiki.js
            "<span class='rejection-date' title='%s'></span>" % self.submission_date.isoformat(),
            )

        message += " You can still get points by clicking on the link and trying again."

        UserNotification.create_error_notification(self.user, message, content_object=self)

        subject = "[%s] Your response to '%s' was not approved" % (
            settings.CHALLENGE.competition_name, self.action.title)

        message = render_to_string("email/rejected_activity.txt", {
            "object": self,
            "COMPETITION_NAME": settings.CHALLENGE.competition_name,
            "domain": settings.CHALLENGE.site_domain,
            })
        html_message = render_to_string("email/rejected_activity.html", {
            "object": self,
            "COMPETITION_NAME": settings.CHALLENGE.competition_name,
            "domain": settings.CHALLENGE.site_domain,
            })

        UserNotification.create_email_notification(self.user.email, subject, message, html_message)

    def post_to_wall(self):
        """post to team wall as system post."""
        team = self.user.get_profile().team
        if team:
            if self.approval_status == "approved":
                # User completed the commitment
                message = "has completed the %s \"%s\"." % (self.action.type,
                                                            self.action.title,)
            else:
                # User is adding the commitment.
                message = "is participating in the %s \"%s\"." % (self.action.type,
                                                                  self.action.title,)

            post = Post(user=self.user,
                        team=team,
                        text=message,
                        style_class="system_post")
            post.save()

    def invalidate_cache(self):
        """Invalidate the categories cache."""
        cache_mgr.delete('smartgrid-levels-%s' % self.user.username)
        cache_mgr.delete('user_events-%s' % self.user.username)
        cache_mgr.invalidate_team_avatar_cache(self.action, self.user)
        cache_mgr.invalidate_commitments_cache(self.user)

    def delete(self, using=None):
        """Custom delete method to remove the points for completed action."""
        profile = self.user.get_profile()

        if self.approval_status == "approved":
            # remove all related point transaction
            profile.remove_related_points(self)
        else:
            # drop any possible signup transaction
            self._drop_signup_points()

        if profile.team:
            message = "is no longer participating in the %s \"%s\"." % (
                self.action.type, self.action.title,)
            post = Post(user=self.user,
                        team=profile.team,
                        text=message,
                        style_class="system_post")
            post.save()

        self.invalidate_cache()

        super(ActionMember, self).delete()


class Reminder(models.Model):
    """
    Sends a reminder for an activity to a user.  Reminders are queued up and sent later.
    """
    REMINDER_CHOICES = (
        ("email", "Email"),
        ("text", "Text"),
        )

    user = models.ForeignKey(User, editable=False)
    action = models.ForeignKey(Action, editable=False)

    send_at = models.DateTimeField(
        help_text="The send time of the reminder."
    )
    sent = models.BooleanField(
        default=False, editable=False,
        help_text="Is reminder sent?")

    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(editable=False, auto_now=True, null=True)

    class Meta:
        """meta"""
        abstract = True
        unique_together = ("user", "action")

    def send(self):
        """send methods that subclass all required to implement."""
        raise NotImplementedError("Reminder subclasses need to implement send.")


class EmailReminder(Reminder):
    """Email Reminder Class"""
    email_address = models.EmailField(
        help_text="The email address."
    )

    def send(self):
        """
        Sends a reminder email to the user.
        """
        if not self.sent:
            subject = "[%s] Reminder for %s" % (settings.CHALLENGE.competition_name,
                                                self.action.title)
            message = render_to_string("email/activity_reminder.txt", {
                "action": self.action,
                "user": self.user,
                "COMPETITION_NAME": settings.CHALLENGE.competition_name,
                "domain": settings.CHALLENGE.site_domain,
                })
            html_message = render_to_string("email/activity_reminder.html", {
                "action": self.action,
                "user": self.user,
                "COMPETITION_NAME": settings.CHALLENGE.competition_name,
                "domain": settings.CHALLENGE.site_domain,
                })

            UserNotification.create_email_notification(self.email_address, subject, message,
                html_message)
            self.sent = True
            self.save()


class TextReminder(Reminder):
    """Text Reminder Class"""
    TEXT_CARRIERS = (
        ('att', 'AT&T'),
        ('sprint', 'Sprint'),
        ('tmobile', 'T-Mobile'),
        ('verizon', 'Verizon'),
        ('mobi', 'Mobi PCS'),
        ('virgin', 'Virgin Mobile'),
        ('alltel', "AllTel"),
        )
    TEXT_EMAILS = {
        "att": "txt.att.net",
        "verizon": "vtext.com",
        "tmobile": "tmomail.net",
        "sprint": "messaging.sprintpcs.com",
        "mobi": "mobipcs.net",
        "virgin": "vmobl.com",
        "alltel": "message.alltel.com",
        }
    text_number = PhoneNumberField(
        help_text="The phone number."
    )
    text_carrier = models.CharField(
        max_length=50, choices=TEXT_CARRIERS, null=True, blank=True,
        help_text="The phone carrier.")

    def send(self):
        """
        Sends a reminder text to the user via an email.
        """
        number = self.text_number.replace("-", "")
        email = number + "@" + self.TEXT_EMAILS[self.text_carrier]
        if not self.sent:
            message = render_to_string("email/activity_text_reminder.txt", {
                "activity": self.action,
                "user": self.user,
                })

            UserNotification.create_email_notification(email, "", message)
            self.sent = True
            self.save()
