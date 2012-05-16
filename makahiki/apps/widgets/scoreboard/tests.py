"""Scoreboard Test."""

import datetime
from django.core.urlresolvers import reverse
from django.test import TransactionTestCase
from apps.managers.challenge_mgr import challenge_mgr
from apps.test_helpers import test_utils


class ScoreboardTest(TransactionTestCase):
    """Scoreboard Test."""
    fixtures = ["test_teams.json"]

    def setUp(self):
        """
        setup
        """
        self.user = test_utils.setup_user(username="user", password="changeme")

        challenge_mgr.register_page_widget("learn", "smartgrid")
        challenge_mgr.register_page_widget("learn", "scoreboard")

        self.client.login(username="user", password="changeme")

    def testScoreboard(self):
        """Test that the scoreboard loads current round information."""

        test_utils.set_competition_round()

        # Give the user points in the round and then check the queryset used in the page.
        profile = self.user.get_profile()
        profile.add_points(10, datetime.datetime.today(), "test")
        profile.save()

        response = self.client.get(reverse("learn_index"))
        self.assertContains(response, "Round 1 Point Scoreboard", count=1,
            msg_prefix="This should display the current round scoreboard.")
        self.assertEqual(response.context["view_objects"]["scoreboard"]["team_standings"][
            0]["profile__team__name"],
            profile.team.name,
            "The user's team should be leading.")
        self.assertEqual(response.context["view_objects"]["scoreboard"]["profile_standings"][
            0]["profile__name"],
            profile.name,
            "The user's should be leading the overall standings.")
        self.assertEqual(response.context["view_objects"]["scoreboard"]["user_team_standings"][0],
            profile,
            "The user should be leading in their own team.")
        self.assertEqual(response.context["view_objects"]["scoreboard"]["team_standings"][
            0]["points"],
            10,
            "The user's team should have 10 points this round.")
        self.assertEqual(response.context["view_objects"]["scoreboard"]["profile_standings"][
            0]["points"], 10,
            "The user should have 10 points this round.")
        self.assertEqual(response.context["view_objects"]["scoreboard"]["user_team_standings"][
                         0].current_round_points(), 10,
            "The user should have 10 points this round.")

        # Get points outside of the round and see if affects the standings.
        profile.add_points(10, datetime.datetime.today() - datetime.timedelta(days=2), "test")
        profile.save()

        response = self.client.get(reverse("learn_index"))
        self.assertEqual(response.context["view_objects"]["scoreboard"]["team_standings"][
            0]["points"],
            10,
            "Test that the user's team still has 10 points.")
        self.assertEqual(response.context["view_objects"]["scoreboard"]["profile_standings"][
            0]["points"], 10,
            "The user still should have 10 points this round.")
        self.assertEqual(response.context["view_objects"]["scoreboard"]["user_team_standings"][
                         0].current_round_points(), 10,
            "The user still should have 10 points this round.")
