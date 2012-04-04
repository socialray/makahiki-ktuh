"""Scoreboard Test."""

import datetime
from django.core.urlresolvers import reverse
from django.test import TransactionTestCase
from django.conf import settings
from apps.test_helpers.test_utils import TestUtils


class ScoreboardTest(TransactionTestCase):
    """Scoreboard Test."""
    fixtures = ["base_teams.json"]

    def setUp(self):
        """
        setup
        """
        self.user = TestUtils.setup_user(username="user", password="changeme")

        TestUtils.register_page_widget("learn", "smartgrid")
        TestUtils.register_page_widget("learn", "notifications")
        TestUtils.register_page_widget("learn", "scoreboard")

        self.client.login(username="user", password="changeme")

    def testScoreboard(self):
        """Test that the scoreboard loads current round information."""
        saved_rounds = settings.COMPETITION_ROUNDS

        TestUtils.set_competition_round()

        # Give the user points in the round and then check the queryset used in the page.
        profile = self.user.get_profile()
        profile.add_points(10, datetime.datetime.today(), "test")
        profile.save()

        response = self.client.get(reverse("learn_index"))
        self.assertContains(response, "Round 1 Scoreboard", count=1,
            msg_prefix="This should display the current round scoreboard.")
        self.assertEqual(response.context["view_objects"]["scoreboard"]["team_standings"][0],
            profile.team,
            "The user's team should be leading.")
        self.assertEqual(response.context["view_objects"]["scoreboard"]["profile_standings"][0],
            profile,
            "The user's should be leading the overall standings.")
        self.assertEqual(response.context["view_objects"]["scoreboard"]["user_team_standings"][0],
            profile,
            "The user should be leading in their own team.")
        self.assertEqual(response.context["view_objects"]["scoreboard"]["team_standings"][0].points,
            10,
            "The user's team should have 10 points this round.")
        self.assertEqual(response.context["view_objects"]["scoreboard"]["profile_standings"][
                         0].current_round_points(), 10,
            "The user should have 10 points this round.")
        self.assertEqual(response.context["view_objects"]["scoreboard"]["user_team_standings"][
                         0].current_round_points(), 10,
            "The user should have 10 points this round.")

        # Get points outside of the round and see if affects the standings.
        profile.add_points(10, datetime.datetime.today() - datetime.timedelta(days=2), "test")
        profile.save()

        response = self.client.get(reverse("learn_index"))
        self.assertEqual(response.context["view_objects"]["scoreboard"]["team_standings"][0].points,
            10,
            "Test that the user's team still has 10 points.")
        self.assertEqual(response.context["view_objects"]["scoreboard"]["profile_standings"][
                         0].current_round_points(), 10,
            "The user still should have 10 points this round.")
        self.assertEqual(response.context["view_objects"]["scoreboard"]["user_team_standings"][
                         0].current_round_points(), 10,
            "The user still should have 10 points this round.")

        # Don't forget to clean up.
        settings.COMPETITION_ROUNDS = saved_rounds
