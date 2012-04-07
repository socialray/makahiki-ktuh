"""Energy Goal Test"""

from apps.managers.team_mgr.models import Group
from apps.managers.player_mgr.models import Profile

from django.test import TransactionTestCase
from django.contrib.auth.models import User

from apps.managers.team_mgr.models import Team
from apps.widgets.energy_goal.models import TeamEnergyGoal


class TeamEnergyGoalTest(TransactionTestCase):
    """Team Energy Goal Test"""
    def setUp(self):
        """setup"""
        group = Group.objects.create(name="Test Group")
        group.save()
        self.team = Team.objects.create(
            group=group,
            name="A"
        )

        self.user = User.objects.create_user("user", "user@test.com")
        profile = self.user.get_profile()
        profile.team = self.team
        profile.save()

    def testTeamEnergyGoal(self):
        """Test energy goal"""
        profile = self.user.get_profile()
        points = profile.points()

        goal = TeamEnergyGoal(
            team=self.team,
            goal_usage=10,
            actual_usage=5,
        )
        goal.save()
        goal.award_goal_points()
        profile = Profile.objects.get(user__username="user")
        self.assertEqual(profile.points(), points,
            "User that did not complete the setup process should not be awarded points.")

        profile.setup_complete = True
        profile.save()

        goal.actual_usage = 15
        goal.save()
        goal.award_goal_points()
        profile = Profile.objects.get(user__username="user")
        self.assertEqual(profile.points(), points,
            "Team that failed the goal should not be awarded any points.")

        goal.actual_usage = 5
        goal.save()
        goal.award_goal_points()
        profile = Profile.objects.get(user__username="user")
        self.assertEqual(profile.points(), points + TeamEnergyGoal.GOAL_POINTS,
            "User that setup their profile should be awarded points.")
