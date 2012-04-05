"""Tests the challenge_mgr module."""

import datetime
from django.contrib.auth.models import User

from django.test import TransactionTestCase
from django.core.urlresolvers import reverse
from django.conf import settings

from apps.managers.challenge_mgr import challenge_mgr
from apps.test_helpers.test_utils import TestUtils


class ContextProcessorFunctionalTestCase(TransactionTestCase):
    """Tests that the proper variables are loaded into a page."""

    def testRoundInfo(self):
        """Tests that round info is available for the page to process."""
        TestUtils.set_competition_round()
        current_round = challenge_mgr.get_current_round()

        User.objects.create_user("user", "user@test.com", password="changeme")
        self.client.login(username="user", password="changeme")

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

        TestUtils.set_competition_round()

        current = challenge_mgr.get_current_round()
        self.assertEqual(current, current_round,
            "Test that the current round is returned.")

        start = datetime.datetime.today() + datetime.timedelta(days=1)
        end = start + datetime.timedelta(days=7)
        settings.COMPETITION_ROUNDS = {
            "Round 1": {"start": start, "end": end, }, }

        current_round = challenge_mgr.get_current_round()
        self.assertTrue(current_round is None,
            "Test that there is no current round.")
