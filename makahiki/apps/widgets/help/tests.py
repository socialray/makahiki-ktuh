"""Tests to see that we can retrieve and display a help topic."""

from django.test import TransactionTestCase
from django.core.urlresolvers import reverse
from apps.managers.cache_mgr import cache_mgr
from apps.managers.challenge_mgr import challenge_mgr
from apps.utils import test_utils

from apps.widgets.help.models import HelpTopic


class HelpFunctionalTestCase(TransactionTestCase):
    """test cases"""

    def setUp(self):
        self.user = test_utils.setup_user(username="user", password="changeme")

        challenge_mgr.register_page_widget("help", "help.rule")
        cache_mgr.clear()

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
