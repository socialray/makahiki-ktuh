"""
test scoreboard
"""

import datetime

from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User
from test_utils import TestUtils
from managers.team_mgr.models import Group, Team
from managers.player_mgr.models import Profile
from managers.score_mgr.models import ScoreboardEntry

class ScoreboardEntryUnitTests(TestCase):
    """scoreboard test"""
    def setUp(self):
        """Generate test. Set the competition settings to the current date for
        testing."""
        self.user = User(username="test_user", password="changeme")
        self.user.save()

        self.saved_rounds = settings.COMPETITION_ROUNDS
        self.current_round = "Round 1"
        TestUtils.set_competition_round()

    def testUserOverallRoundRankWithPoints(self):
        """Tests that the overall rank calculation for a user in a round is correct based on
        points."""
        top_entry = ScoreboardEntry.objects.filter(round_name=self.current_round).order_by(
            "-points")[0]
        entry = ScoreboardEntry.objects.get_or_create(
            profile=self.user.get_profile(),
            round_name=self.current_round,
        )
        entry.points = top_entry.points + 1
        entry.last_awarded_submission = datetime.datetime.today()
        entry.save()

        self.assertEqual(ScoreboardEntry.user_round_overall_rank(self.user,
            self.current_round), 1,
            "Check user is ranked #1 for the current round.")

        user2 = User(username="test_user2", password="changeme")
        user2.save()

        profile2 = user2.get_profile()
        entry2 = ScoreboardEntry.objects.get_or_create(
            profile=profile2,
            round_name=self.current_round,
        )
        entry2.points = entry.points + 1
        entry2.last_awarded_submission = entry.last_awarded_submission
        entry2.save()

        self.assertEqual(ScoreboardEntry.user_round_overall_rank(self.user,
            self.current_round), 2,
            "Check user is now second.")

    def testUserOverallRoundRankWithSubmissionDate(self):
        """Tests that the overall rank calculation for a user in a round is correct based on
        submission date."""
        top_entry = ScoreboardEntry.objects.filter(round_name=self.current_round).order_by(
            "-points")[0]
        entry = ScoreboardEntry.objects.get_or_create(
            profile=self.user.get_profile(),
            round_name=self.current_round,
        )
        entry.points = top_entry.points + 1
        entry.last_awarded_submission = datetime.datetime.today() - datetime.timedelta(
            days=3)
        entry.save()

        self.assertEqual(ScoreboardEntry.user_round_overall_rank(self.user,
            self.current_round), 1,
            "Check user is ranked #1 for the current round.")

        user2 = User(username="test_user2", password="changeme")
        user2.save()

        profile2 = user2.get_profile()
        entry2 = ScoreboardEntry.objects.get_or_create(
            profile=profile2,
            round_name=self.current_round,
        )
        entry2.points = entry.points
        entry2.last_awarded_submission = datetime.datetime.today()
        entry2.save()

        self.assertEqual(ScoreboardEntry.user_round_overall_rank(self.user,
            self.current_round), 2,
            "Check user is now second.")

    def testUserTeamRoundRankWithPoints(self):
        """Tests that the team rank calculation for a round is correct based on points."""
        # Setup dorm
        group = Group(name="Test group")
        group.save()
        team = Team(number="A", group=group)
        team.save()

        profile = self.user.get_profile()
        profile.team = team
        profile.save()

        # Set up entry
        top_entry = ScoreboardEntry.objects.filter(round_name=self.current_round).order_by(
            "-points")[0]
        entry = ScoreboardEntry.objects.get_or_create(
            profile=self.user.get_profile(),
            round_name=self.current_round,
        )
        entry.points = top_entry.points + 1
        entry.last_awarded_submission = datetime.datetime.today()
        entry.save()

        self.assertEqual(
            ScoreboardEntry.user_round_team_rank(self.user, self.current_round)
            , 1,
            "Check user is ranked #1 for the current round.")

        user2 = User(username="test_user2", password="changeme")
        user2.save()
        profile2 = user2.get_profile()
        profile2.team = team
        profile2.save()

        entry2 = ScoreboardEntry.objects.get_or_create(
            profile=profile2,
            round_name=self.current_round,
        )
        entry2.points = entry.points + 1
        entry2.last_awarded_submission = entry.last_awarded_submission
        entry2.save()

        self.assertEqual(
            ScoreboardEntry.user_round_team_rank(self.user, self.current_round)
            , 2,
            "Check user is now second.")

    def testUserTeamRoundRankWithSubmissionDate(self):
        """Tests that the team rank calculation for a round is correct based on points."""
        # Set up dorm
        group = Group(name="Test group")
        group.save()
        team = Team(number="A", group=group)
        team.save()

        # Create the entry for the test user
        profile = self.user.get_profile()
        profile.team = team
        profile.save()
        top_entry = ScoreboardEntry.objects.filter(round_name=self.current_round).order_by(
            "-points")[0]
        entry = ScoreboardEntry.objects.get_or_create(
            profile=self.user.get_profile(),
            round_name=self.current_round,
        )
        entry.points = top_entry.points + 1
        entry.last_awarded_submission = datetime.datetime.today() - datetime.timedelta(
            days=3)
        entry.save()

        # Create another test user
        user2 = User(username="test_user2", password="changeme")
        user2.save()
        profile2 = user2.get_profile()
        profile2.team = team
        profile2.save()

        entry2 = ScoreboardEntry.objects.get_or_create(
            profile=profile2,
            round_name=self.current_round,
        )
        entry2.points = entry.points
        entry2.last_awarded_submission = datetime.datetime.today()
        entry2.save()

        self.assertEqual(
            ScoreboardEntry.user_round_team_rank(self.user, self.current_round)
            , 2,
            "Check user is now second.")

    def testRoundRankWithoutEntry(self):
        """Tests that the overall rank calculation is correct even if a user has not done
        anything yet."""
        group = Group(name="Test group")
        group.save()
        team = Team(number="A", group=group)
        team.save()

        # Rank will be the number of users who have points plus one.
        overall_rank = Profile.objects.filter(points__gt=0).count() + 1
        team_rank = Profile.objects.filter(points__gt=0,
            team=team).count() + 1

        self.assertEqual(ScoreboardEntry.user_round_overall_rank(self.user,
            self.current_round), overall_rank,
            "Check user is last overallfor the current round.")
        self.assertEqual(
            ScoreboardEntry.user_round_team_rank(self.user, self.current_round)
            , team_rank,
            "Check user is last in their team for the current round.")

        user2 = User(username="test_user2", password="changeme")
        user2.save()

        profile2 = user2.get_profile()
        entry2 = ScoreboardEntry.objects.get_or_create(
            profile=profile2,
            round_name=self.current_round,
        )
        entry2.points = 10
        entry2.last_awarded_submission = datetime.datetime.today()
        entry2.team = team
        entry2.save()

        self.assertEqual(ScoreboardEntry.user_round_overall_rank(self.user,
            self.current_round), overall_rank + 1,
            "Check that the user's overall rank has moved down.")
        self.assertEqual(
            ScoreboardEntry.user_round_team_rank(self.user, self.current_round)
            , team_rank + 1,
            "Check that the user's team rank has moved down.")

    def tearDown(self):
        """Restore the saved settings."""
        settings.COMPETITION_ROUNDS = self.saved_rounds
    