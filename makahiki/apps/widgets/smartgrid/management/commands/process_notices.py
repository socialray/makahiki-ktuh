"""Process Notice command."""

import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from django.core import management
from django.core.urlresolvers import reverse
from apps.widgets.smartgrid.models import CommitmentMember, ActivityMember
from apps.widgets.notifications.models import UserNotification, NoticeTemplate
from apps.managers.challenge_mgr import challenge_mgr
from django.db.models import Q


def notify_round_started():
    """notify the start of a round"""
    if not challenge_mgr.in_competition():
        return

    today = datetime.datetime.today()
    current_round = "Overall Round"
    previous_round = 'Overall Round'

    for key, value in settings.COMPETITION_ROUNDS.items():
        # We're looking for a round that ends today and another that starts
        # today (or overall)
        start = value["start"]
        end = value["end"]
        # Check yesterday's round and check for the current round.
        if start < (today - datetime.timedelta(days=1)) < end:
            previous_round = key

        if start < today < end:
            current_round = key

    print 'Previous Round: %s' % previous_round
    print 'Current Round: %s' % current_round

    if current_round and previous_round and current_round != previous_round:
        print 'Sending out round transition notices.'
        template = NoticeTemplate.objects.get(notice_type="round-transition")
        message = template.render({"PREVIOUS_ROUND": previous_round,
                                   "CURRENT_ROUND": current_round, })
        for user in User.objects.all():
            UserNotification.create_info_notification(user, message,
                                                      display_alert=True, )


def notify_commitment_end():
    """notify the end of a commitment period and award points"""
    members = CommitmentMember.objects.filter(
        completion_date=datetime.date.today(), award_date__isnull=True)

    # try and load the notification template.
    template = None
    try:
        template = NoticeTemplate.objects.get(notice_type="commitment-ready")
    except NoticeTemplate.DoesNotExist:
        pass

    for member in members:
        message = None
        if template:
            message = template.render({"COMMITMENT": member.commitment})
        else:
            message = "Your commitment <a href='%s'>%s</a> has end." % (
                reverse("activity_task",
                        args=(member.commitment.type, member.commitment.slug,
                            )),
                member.commitment.title)

            message += "You can click on the link to claim your points."

        UserNotification.create_info_notification(member.user, message,
                                                  display_alert=True,
                                                  content_object=member)
        print "created commitment end notification for %s : %s" % (
            member.user, member.commitment.slug)


def process_rsvp():
    """process RSVP notification and penalty"""
    members = ActivityMember.objects.filter(
        Q(activity__type="event") | Q(activity__type="excursion"),
        approval_status="pending")

    # try and load the notification template.
    template_noshow = None
    try:
        template_noshow = NoticeTemplate.objects.get(
            notice_type="event-noshow-penalty")
    except NoticeTemplate.DoesNotExist:
        pass

    template_reminder = None
    try:
        template_reminder = NoticeTemplate.objects.get(
            notice_type="event-post-reminder")
    except NoticeTemplate.DoesNotExist:
        pass

    for member in members:
        activity = member.activity
        user = member.user
        profile = user.get_profile()

        diff = datetime.date.today() - activity.event_date.date()
        if diff.days == 3:
            message = "%s: %s (No Show)" % (
                activity.type.capitalize(), activity.title)
            profile.remove_points(4,
                                  datetime.datetime.today() - datetime
                                  .timedelta(
                                      minutes=1), message, member)
            profile.save()
            print "removed 4 points from %s for '%s'" % (profile.name, message)

            if template_noshow:
                message = template_noshow.render({"ACTIVITY": activity})
            else:
                message = "4 points had been deducted from you, "\
                          "because you signed up but did not enter the "\
                          "confirmation code 2 days after the %s <a "\
                          "href='%s'>%s</a>, " % (
                    activity.type.capitalize(),
                    reverse("activity_task",
                            args=(activity.type, activity.slug,)),
                    activity.title)
                message += " If you did attend, please click on the link to "\
                           "claim your points and reverse the deduction."

            UserNotification.create_info_notification(user, message,
                                                      display_alert=True,
                                                      content_object=member)
            print "created no-show penalty notification for %s for %s" % (
                profile.name, activity.title)

        if diff.days == 2:
            if template_reminder:
                message = template_reminder.render({"ACTIVITY": activity})
            else:
                message = "Hi %s, <p/> We just wanted to remind you that the "\
                          "%s <a href='http://%s%s'>%s</a> had ended. Please "\
                          "click on the link to claim your points." % (
                    profile.name,
                    activity.type.capitalize(),
                    Site.objects.get(id=settings.SITE_ID).domain,
                    reverse("activity_task",
                            args=(activity.type, activity.slug,)),
                    activity.title)
                message += "<p/>Because you signed up for the "\
                           "event/excursion, if you do not enter the "\
                           "confirmation code within 2 days after the "\
                           "event/excusion, a total of 4 points (2 point "\
                           "signup bonus plus 2 point no-show penalty) will "\
                           "be deducted from your total points. So please "\
                           "enter your confirmation code early to avoid the "\
                           "penalty."
                message += "<p/><p/>Kukui Cup Administrators"
            subject = "[Kukui Cup] Reminder to enter your event/excursion "\
                      "confirmation code"
            UserNotification.create_email_notification(user.email, subject,
                                                       message, message)
            print "sent post event email reminder to %s for %s" % (
                profile.name, activity.title)


class Command(management.base.BaseCommand):
    """command."""
    help = 'Process notification for RSVP, commitment and round starting.'

    def handle(self, *args, **options):
        """Process notification for RSVP, commitment and round starting."""

        self.stdout.write('****** Processing RSVPs for %s *******\n' % datetime.datetime.today())

        process_rsvp()

        self.stdout.write('****** Processing commitment notifications for %s *******\n' %
                          datetime.datetime.today())
        notify_commitment_end()

        self.stdout.write('****** Processing round notifications for %s *******\n' %
              datetime.datetime.today())
        notify_round_started()
