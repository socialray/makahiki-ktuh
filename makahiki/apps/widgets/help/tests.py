"""Tests to see that we can retrieve and display a help topic."""

from django.test import TransactionTestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from apps.managers.team_mgr.models import Team
from apps.widgets.help.models import HelpTopic
from apps.test_helpers.test_utils import TestUtils


class HelpFunctionalTestCase(TransactionTestCase):
    """test cases"""
    fixtures = ["base_teams.json"]

    def setUp(self):
        self.user = User.objects.create_user("user", "user@test.com",
                                             password="changeme")
        team = Team.objects.all()[0]
        profile = self.user.get_profile()
        profile.team = team
        profile.setup_complete = True
        profile.setup_profile = True
        profile.save()

        TestUtils.register_page_widget("help", "help.rule")

        self.client.login(username="user", password="changeme")

    def testIndex(self):
        """Check that we can load the index page."""
        response = self.client.get(reverse("help_index"))
        self.failUnlessEqual(response.status_code, 200)

    def testTopic(self):
        """Check that we can view a help topic."""
        topic = HelpTopic(
            title="A topic",
            slug="a-topic",
            category="rules",
            contents="This is a topic",
        )
        topic.save()

        response = self.client.get(reverse("help_index"))
        self.assertContains(response, topic.title,
                            msg_prefix="Page should have topic listed.")
        response = self.client.get(reverse("help_topic",
                                           args=(topic.category, topic.slug)))
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, topic.contents)
