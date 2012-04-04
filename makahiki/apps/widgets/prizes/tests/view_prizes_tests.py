"""Prize page view test"""
import datetime

from django.test import TransactionTestCase
from django.core.urlresolvers import reverse
from django.conf import settings

from apps.widgets.prizes.models import Prize
from apps.test_helpers.test_utils import TestUtils


class PrizesFunctionalTestCase(TransactionTestCase):
    """test prize page view"""
    fixtures = ["base_teams.json", "test_prizes.json"]

    def setUp(self):
        """Set up a team and log in."""
        self.user = TestUtils.setup_user(username="user", password="changeme")

        TestUtils.set_competition_round()
        TestUtils.register_page_widget("win", "prizes")

        profile = self.user.get_profile()
        profile.add_points(10, datetime.datetime.today(), "test")
        profile.save()

        self.client.login(username="user", password="changeme")

    def testIndex(self):
        """Check that we can load the index page."""
        response = self.client.get(reverse("win_index"))
        self.failUnlessEqual(response.status_code, 200)

        for prize in Prize.objects.all():
            self.assertContains(response, prize.title, msg_prefix="Prize not found on prize page")

    def testLeadersInRound1(self):
        """Test that the leaders are displayed correctly in round 1."""
        start = datetime.datetime.today()
        end1 = start + datetime.timedelta(days=7)
        end2 = start + datetime.timedelta(days=14)

        settings.COMPETITION_ROUNDS = {
            "Round 1": {"start": start,
                        "end": end1, },
            "Round 2": {"start": end1,
                        "end": end2, },
            "Overall": {"start": start,
                        "end": end2, },
            }
        settings.COMPETITION_START = start
        settings.COMPETITION_END = end2

        profile = self.user.get_profile()
        profile.name = "Test User"
        profile.add_points(10, datetime.datetime.today(), "test")
        team = profile.team
        profile.save()

        response = self.client.get(reverse("win_index"))
        self.assertContains(response, "Current leader: " + str(profile), count=2,
            msg_prefix="Individual prizes should have user as the leader.")
        self.assertContains(response, "Current leader: " + str(team), count=1,
            msg_prefix="Team points prizes should have team as the leader")
        self.assertContains(response, "Current leader: <span id='round-1-leader'></span>", count=1,
            msg_prefix="Span for round 1 energy prize should be inserted.")
        self.assertNotContains(response, "Current leader: <span id='round-2-leader'></span>",
            msg_prefix="Span for round 2 energy prize should not be inserted.")
        self.assertContains(response, "Current leader: <span id='overall-leader'></span>", count=1,
            msg_prefix="Span for overall energy prize should be inserted.")
        self.assertContains(response, "Current leader: TBD", count=3,
            msg_prefix="Round 2 prizes should not have a leader yet.")

        # Test XSS vulnerability.
        profile.name = '<div id="xss-script"></div>'
        profile.save()

        response = self.client.get(reverse("win_index"))
        self.assertNotContains(response, profile.name,
            msg_prefix="<div> tag should be escaped.")

    def testLeadersInRound2(self):
        """Test that the leaders are displayed correctly in round 2."""

        TestUtils.set_two_rounds()

        profile = self.user.get_profile()
        profile.add_points(10, datetime.datetime.today(), "test")
        profile.name = "Test User"
        team = profile.team
        profile.save()

        response = self.client.get(reverse("win_index"))
        self.assertContains(response, "Winner: ", count=3,
            msg_prefix="There should be winners for three prizes.")
        self.assertContains(response, "Current leader: " + str(profile), count=1,
            msg_prefix="Individual prizes should have user as the leader.")
        self.assertContains(response, "Current leader: <span id='round-2-leader'></span>", count=1,
            msg_prefix="Span for round 2 energy prize should be inserted.")
        self.assertContains(response, "Current leader: " + str(team), count=1,
            msg_prefix="Team points prizes should have team as the leader")

        # Test XSS vulnerability.
        profile.name = '<div id="xss-script"></div>'
        profile.save()

        response = self.client.get(reverse("win_index"))
        self.assertNotContains(response, profile.name,
            msg_prefix="<div> tag should be escaped.")
