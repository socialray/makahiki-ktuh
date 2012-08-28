"""Tests the challenge_mgr module."""

import datetime
from django.contrib.auth.models import User

from django.test import TransactionTestCase
from django.core.urlresolvers import reverse

from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.challenge_mgr.models import RoundSetting
from apps.utils import test_utils


class ContextProcessorFunctionalTestCase(TransactionTestCase):
    """Tests that the proper variables are loaded into a page."""

    def testRoundInfo(self):
        """Tests that round info is available for the page to process."""
        challenge_mgr.init()
        test_utils.set_competition_round()
        current_round = challenge_mgr.get_round_name()

        User.objects.create_user("user", "user@test.com", password="changeme")
        self.client.login(username="user", password="changeme")

        challenge_mgr.register_page_widget("home", "home")
        response = self.client.get(reverse("home_index"))
        # Response context should have round info corresponding to the past days.

        self.assertEqual(response.context["CURRENT_ROUND_INFO"]["name"], current_round,
            "Expected %s but got %s" % (
                current_round, response.context["CURRENT_ROUND_INFO"]["name"]))


class BaseUnitTestCase(TransactionTestCase):
    """basic setting test"""
    def testCurrentRound(self):
        """Tests that the current round retrieval is correct."""
        current_round = "Round 1"

        test_utils.set_competition_round()

        current = challenge_mgr.get_round_name()
        self.assertEqual(current, current_round,
            "Test that the current round is returned.")

        start = datetime.datetime.today() + datetime.timedelta(days=1)
        end = start + datetime.timedelta(days=7)
        rounds = RoundSetting.objects.get(name="Round 1")
        rounds.start = start
        rounds.end = end
        rounds.save()

        challenge_mgr.init()
        current_round = challenge_mgr.get_round_name()
        self.assertTrue(current_round is None,
            "Test that there is no current round.")
