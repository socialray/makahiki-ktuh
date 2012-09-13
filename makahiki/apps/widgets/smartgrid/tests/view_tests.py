"""View Test."""
import datetime
from django.core.urlresolvers import reverse
from django.test import TransactionTestCase
from apps.managers.challenge_mgr import challenge_mgr
from apps.utils import test_utils
from apps.widgets.smartgrid.models import  EmailReminder, ActionMember, \
                                           TextReminder, Commitment, ConfirmationCode
from apps.managers.player_mgr.models import Profile


class ActivitiesFunctionalTest(TransactionTestCase):
    """Activities View Test."""

    def setUp(self):
        """setup"""
        self.user = self.user = test_utils.setup_user(username="user", password="changeme")

        challenge_mgr.register_page_widget("learn", "smartgrid")

        from apps.managers.cache_mgr import cache_mgr
        cache_mgr.clear()

        self.client.login(username="user", password="changeme")

    def testIndex(self):
        """Check that we can load the index page."""
        response = self.client.get(reverse("learn_index"))
        self.failUnlessEqual(response.status_code, 200)

    def testViewCodesAndRsvps(self):
        """test view code and rsvp."""
        activity = test_utils.create_event()

        ConfirmationCode.generate_codes_for_activity(activity, 5)

        response = self.client.get(
            reverse('activity_view_codes', args=(activity.type, activity.id)))
        self.failUnlessEqual(response.status_code, 404)
        response = self.client.get(
            reverse('activity_view_rsvps', args=(activity.type, activity.id)))
        self.assertEqual(response.status_code, 404)

        self.user.is_staff = True
        self.user.save()

        response = self.client.get(
            reverse('activity_view_codes', args=(activity.type, activity.id)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/view_codes.html')

        response = self.client.get(
            reverse('activity_view_rsvps', args=(activity.type, activity.id)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/rsvps.html')

    def testConfirmationCode(self):
        """
        Tests the submission of a confirmation code.
        """
        activity = test_utils.create_event()
        activity.event_date = datetime.datetime.today() - datetime.timedelta(days=1, seconds=30)
        activity.save()

        ConfirmationCode.generate_codes_for_activity(activity, 10)
        code = ConfirmationCode.objects.filter(action=activity)[0]

        response = self.client.post(reverse("activity_add_task", args=("event", "test-event")), {
            "response": code.code,
            "code": 1,
            }, follow=True)

        self.failUnlessEqual(response.status_code, 200)
        self.assertEqual(ConfirmationCode.objects.filter(
            action=activity, is_active=False).count(), 1)
        code = ConfirmationCode.objects.filter(action=activity)[0]
        self.assertTrue(
            activity.action_ptr in self.user.action_set.filter(
                actionmember__award_date__isnull=False))

        # Try submitting the code again and check if we have an error message.
        code = ConfirmationCode.objects.filter(action=activity)[1]
        response = self.client.post(reverse("activity_add_task", args=("event", "test-event")), {
            "response": code.code,
            "code": 1,
            }, follow=True)
        self.assertContains(response, "You have already redeemed a code for this action.")

        # Try creating a new activity with codes and see if we can submit a code for one activity
        # for another.
        code = ConfirmationCode.objects.filter(action=activity)[2]
        activity = test_utils.create_event(slug="test-event2")
        activity.event_date = datetime.datetime.today() - datetime.timedelta(days=1, seconds=30)
        activity.save()
        ConfirmationCode.generate_codes_for_activity(activity, 1)

        response = self.client.post(reverse("activity_add_task", args=("event", "test-event2")),
                {
                "response": code.code,
                "code": 1,
                }, follow=True)
        self.assertContains(response, "This confirmation code is not valid for this action.")

    def testRejectedActivity(self):
        """
        Test that a rejected activity submission posts a message.
        """
        activity = test_utils.create_activity()
        member = ActionMember(
            action=activity,
            user=self.user,
            approval_status="rejected",
            submission_date=datetime.datetime.today(),
        )
        member.save()
        response = self.client.get(reverse("learn_index"))
        self.assertContains(response, 'Your response to <a href="%s' % (
            reverse("activity_task", args=(activity.type, activity.slug,)),
            ))
        response = self.client.get(reverse("learn_index"))
        self.assertNotContains(response, "notification-box")

    def testAddCommitment(self):
        """
        Test that the user can add a commitment.
        """
        commitment = Commitment(
            title="Test commitment",
            slug="test-commitment",
            description="A commitment!",
            point_value=10,
            type="commitment",
        )
        commitment.save()

        response = self.client.post(
            reverse("activity_add_task", args=(commitment.type, commitment.slug,)), follow=True)
        self.failUnlessEqual(response.status_code, 200)

        points = Profile.objects.get(user=self.user).points
        response = self.client.post(
            reverse("activity_add_task", args=(commitment.type, commitment.slug,)), follow=True)
        self.failUnlessEqual(response.status_code, 200)

        self.assertEqual(points, Profile.objects.get(user=self.user).points)

    def testAddEmailReminder(self):
        """
        Test that the user can create a email reminder.
        """
        event = test_utils.create_event()

        reminders = self.user.emailreminder_set.count()

        # Test invalid forms
        response = self.client.post(reverse("activity_reminder", args=(event.type, event.slug,)), {
            "send_email": True,
            "email": "",
            "email_advance": "1",
            "send_text": False,
            "text_advance": "1",
            }, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, "A valid email address is required.",
            count=1, msg_prefix="Error text should be displayed.")
        self.assertEqual(self.user.emailreminder_set.count(), reminders,
            "Should not have added a reminder")

        response = self.client.post(reverse("activity_reminder", args=(event.type, event.slug,)), {
            "send_email": True,
            "email": "foo",
            "email_advance": "1",
            "send_text": False,
            "text_advance": "1",
            }, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, "A valid email address is required.",
            count=1, msg_prefix="Error text should be displayed.")
        self.assertEqual(self.user.emailreminder_set.count(), reminders,
            "Should not have added a reminder")

        # Test valid form
        response = self.client.post(reverse("activity_reminder", args=(event.type, event.slug,)),
                {
            "send_email": True,
            "email": "foo@test.com",
            "email_advance": "1",
            "send_text": False,
            "text_advance": "1",
            }, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.failUnlessEqual(response.status_code, 200)
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.user.email, "foo@test.com",
            "Profile should now have a contact email.")
        self.assertEqual(self.user.emailreminder_set.count(), reminders + 1,
            "Should have added a reminder")

    def testChangeEmailReminder(self):
        """
        Test that we can adjust a reminder.
        """
        event = test_utils.create_event()

        original_date = event.event_date - datetime.timedelta(hours=2)
        reminder = EmailReminder(
            user=self.user,
            action=event,
            email_address="foo@foo.com",
            send_at=original_date,
        )
        reminder.save()
        reminder_count = self.user.emailreminder_set.count()

        response = self.client.post(reverse("activity_reminder", args=(event.type, event.slug,)), {
            "send_email": True,
            "email": "foo@test.com",
            "email_advance": "1",
            "send_text": False,
            "text_advance": "1",
            }, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.failUnlessEqual(response.status_code, 200)

        reminder = self.user.emailreminder_set.get(action=event)
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(reminder.email_address, "foo@test.com",
            "Email address should have changed.")
        self.assertEqual(profile.user.email, "foo@test.com",
            "Profile email address should have changed.")
        self.assertNotEqual(reminder.send_at, original_date, "Send time should have changed.")
        self.assertEqual(self.user.emailreminder_set.count(), reminder_count,
            "No new reminders should have been created.")

    def testRemoveEmailReminder(self):
        """
        Test that unchecking send_email will remove the reminder.
        """
        event = test_utils.create_event()

        reminder = EmailReminder(
            user=self.user,
            action=event,
            email_address="foo@foo.com",
            send_at=event.event_date - datetime.timedelta(hours=2),
        )
        reminder.save()
        reminder_count = self.user.emailreminder_set.count()

        response = self.client.post(reverse("activity_reminder", args=(event.type, event.slug,)), {
            "send_email": False,
            "email": "",
            "email_advance": "1",
            "send_text": False,
            "text_advance": "1",
            }, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.failUnlessEqual(response.status_code, 200)

        self.assertEqual(self.user.emailreminder_set.count(), reminder_count - 1,
            "User should not have a reminder.")

    def testAddTextReminder(self):
        """
        Test that a user can create a text reminder.
        """
        event = test_utils.create_event()

        reminders = self.user.textreminder_set.count()

        # Test invalid forms
        response = self.client.post(reverse("activity_reminder", args=(event.type, event.slug,)), {
            "send_email": False,
            "email": "",
            "email_advance": "1",
            "send_text": True,
            "text_number": "",
            "text_carrier": "att",
            "text_advance": "1",
            }, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, "A valid phone number is required.",
            count=1, msg_prefix="Error text should be displayed.")
        self.assertEqual(self.user.textreminder_set.count(), reminders,
            "Should not have added a reminder")

        response = self.client.post(reverse("activity_reminder", args=(event.type, event.slug,)), {
            "send_email": False,
            "email": "",
            "email_advance": "1",
            "send_text": True,
            "text_number": "555",
            "text_carrier": "att",
            "text_advance": "1",
            }, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, "A valid phone number is required.",
            count=1, msg_prefix="Error text should be displayed.")
        self.assertEqual(self.user.textreminder_set.count(), reminders,
            "Should not have added a reminder")

        # Test valid form
        response = self.client.post(reverse("activity_reminder", args=(event.type, event.slug,)), {
            "send_email": False,
            "email": "",
            "email_advance": "1",
            "send_text": True,
            "text_number": "808-555-1234",
            "text_carrier": "att",
            "text_advance": "1",
            }, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        self.failUnlessEqual(response.status_code, 200)
        self.assertEqual(self.user.textreminder_set.count(), reminders + 1,
            "Should have added a reminder")
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.contact_text, "808-555-1234",
            "Check that the user now has a contact number.")
        self.assertEqual(profile.contact_carrier, "att",
            "Check that the user now has a contact carrier.")

    def testChangeTextReminder(self):
        """
        Test that we can adjust a text reminder.
        """
        event = test_utils.create_event()

        original_date = event.event_date - datetime.timedelta(hours=2)
        reminder = TextReminder(
            user=self.user,
            action=event,
            text_number="8085551234",
            text_carrier="att",
            send_at=original_date,
        )
        reminder.save()
        reminder_count = self.user.textreminder_set.count()

        response = self.client.post(reverse("activity_reminder", args=(event.type, event.slug,)), {
            "send_email": False,
            "email": "",
            "email_advance": "1",
            "send_text": True,
            "text_number": "18085556789",
            "text_carrier": "sprint",
            "text_advance": "1",
            }, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        self.failUnlessEqual(response.status_code, 200)
        reminder = self.user.textreminder_set.get(action=event)
        # print profile.contact_text
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(reminder.text_number, "808-555-6789", "Text number should have updated.")
        self.assertEqual(profile.contact_text, "808-555-6789",
            "Profile text number should have updated.")
        self.assertNotEqual(reminder.send_at, original_date, "Send time should have changed.")
        self.assertEqual(self.user.textreminder_set.count(), reminder_count,
            "No new reminders should have been created.")

    def testRemoveTextReminder(self):
        """
        Test that we can adjust a text reminder.
        """
        event = test_utils.create_event()

        reminder = TextReminder(
            user=self.user,
            action=event,
            text_number="8085551234",
            text_carrier="att",
            send_at=event.event_date - datetime.timedelta(hours=2),
        )
        reminder.save()
        reminder_count = self.user.textreminder_set.count()

        response = self.client.post(reverse("activity_reminder", args=(event.type, event.slug,)), {
            "send_email": False,
            "email": "",
            "email_advance": "1",
            "send_text": False,
            "text_number": "",
            "text_carrier": "sprint",
            "text_advance": "1",
            }, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        self.failUnlessEqual(response.status_code, 200)
        self.assertEqual(self.user.textreminder_set.count(), reminder_count - 1,
            "User should not have a reminder.")
