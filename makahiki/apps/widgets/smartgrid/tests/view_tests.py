"""View Test."""
import datetime
from django.core.urlresolvers import reverse
from django.test import TestCase
from apps.widgets.smartgrid.models import  EmailReminder, ActivityMember, \
                                           TextReminder, Commitment, ConfirmationCode
from apps.managers.player_mgr.models import Profile
from apps.test_helpers.test_utils import TestUtils


class ActivitiesFunctionalTest(TestCase):
    """Activities View Test."""
    fixtures = ["base_teams.json"]

    def setUp(self):
        """setup"""
        self.user = self.user = TestUtils.setup_user(username="user", password="changeme")

        TestUtils.register_page_widget("learn", "smartgrid")
        TestUtils.register_page_widget("learn", "notifications")

        self.client.login(username="user", password="changeme")

    def testIndex(self):
        """Check that we can load the index page."""
        response = self.client.get(reverse("learn_index"))
        self.failUnlessEqual(response.status_code, 200)

    def testViewCodesAndRsvps(self):
        """test view code and rsvp."""
        activity = TestUtils.create_event()

        ConfirmationCode.generate_codes_for_activity(activity, 5)

        response = self.client.get(
            reverse('activity_view_codes', args=(activity.type, activity.slug)))
        self.failUnlessEqual(response.status_code, 404)
        response = self.client.get(
            reverse('activity_view_rsvps', args=(activity.type, activity.slug)))
        self.assertEqual(response.status_code, 404)

        self.user.is_staff = True
        self.user.save()

        response = self.client.get(
            reverse('activity_view_codes', args=(activity.type, activity.slug)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_codes.html')

        response = self.client.get(
            reverse('activity_view_rsvps', args=(activity.type, activity.slug)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rsvps.html')

    def testConfirmationCode(self):
        """
        Tests the submission of a confirmation code.
        """
        activity = TestUtils.create_event(slug="test-activity")
        activity.event_date = datetime.datetime.today() - datetime.timedelta(days=1, seconds=30)
        activity.save()

        ConfirmationCode.generate_codes_for_activity(activity, 10)
        code = ConfirmationCode.objects.filter(activity=activity)[0]

        response = self.client.post(reverse("activity_add_task", args=("event", "test-activity")), {
            "response": code.code,
            "code": 1,
            }, follow=True)

        self.failUnlessEqual(response.status_code, 200)
        self.assertEqual(ConfirmationCode.objects.filter(
            activity=activity, is_active=False).count(), 1)
        code = ConfirmationCode.objects.filter(activity=activity)[0]
        self.assertTrue(
            activity in self.user.activity_set.filter(activitymember__award_date__isnull=False))

        # Try submitting the code again and check if we have an error message.
        code = ConfirmationCode.objects.filter(activity=activity)[1]
        response = self.client.post(reverse("activity_add_task", args=("event", "test-activity")), {
            "response": code.code,
            "code": 1,
            }, follow=True)
        self.assertContains(response, "You have already redemmed a code for this activity.")

        # Try creating a new activity with codes and see if we can submit a code for one activity
        # for another.
        code = ConfirmationCode.objects.filter(activity=activity)[2]
        activity = TestUtils.create_event(slug="test-activity2")
        activity.event_date = datetime.datetime.today() - datetime.timedelta(days=1, seconds=30)
        activity.save()
        ConfirmationCode.generate_codes_for_activity(activity, 1)

        response = self.client.post(reverse("activity_add_task", args=("event", "test-activity2")),
                {
                "response": code.code,
                "code": 1,
                }, follow=True)
        self.assertContains(response, "This confirmation code is not valid for this activity.")

    def testRejectedActivity(self):
        """
        Test that a rejected activity submission posts a message.
        """
        activity = TestUtils.create_activity()
        member = ActivityMember(
            activity=activity,
            user=self.user,
            approval_status="rejected",
            submission_date=datetime.datetime.today(),
        )
        member.save()
        response = self.client.get(reverse("learn_index"))
        self.assertContains(response, "Your response to <a href='%s'>%s</a>" % (
            reverse("activity_task", args=(activity.type, activity.slug,)),
            activity.title,
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
        event = TestUtils.create_event()

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
        response = self.client.post(reverse("activity_reminder", args=(event.type, event.slug,)), {
            "send_email": True,
            "email": "foo@test.com",
            "email_advance": "1",
            "send_text": False,
            "text_advance": "1",
            }, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.failUnlessEqual(response.status_code, 200)
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.contact_email, "foo@test.com",
            "Profile should now have a contact email.")
        self.assertEqual(self.user.emailreminder_set.count(), reminders + 1,
            "Should have added a reminder")

    def testChangeEmailReminder(self):
        """
        Test that we can adjust a reminder.
        """
        event = TestUtils.create_event()

        original_date = event.event_date - datetime.timedelta(hours=2)
        reminder = EmailReminder(
            user=self.user,
            activity=event,
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

        reminder = self.user.emailreminder_set.get(activity=event)
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(reminder.email_address, "foo@test.com",
            "Email address should have changed.")
        self.assertEqual(profile.contact_email, "foo@test.com",
            "Profile email address should have changed.")
        self.assertNotEqual(reminder.send_at, original_date, "Send time should have changed.")
        self.assertEqual(self.user.emailreminder_set.count(), reminder_count,
            "No new reminders should have been created.")

    def testRemoveEmailReminder(self):
        """
        Test that unchecking send_email will remove the reminder.
        """
        event = TestUtils.create_event()

        reminder = EmailReminder(
            user=self.user,
            activity=event,
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
        event = TestUtils.create_event()

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
        event = TestUtils.create_event()

        original_date = event.event_date - datetime.timedelta(hours=2)
        reminder = TextReminder(
            user=self.user,
            activity=event,
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
        reminder = self.user.textreminder_set.get(activity=event)
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
        event = TestUtils.create_event()

        reminder = TextReminder(
            user=self.user,
            activity=event,
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
