"""Energy scoreboard Test"""

from django.test import TransactionTestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from apps.managers.team_mgr.models import Team
from apps.widgets.energy_goal.models import TeamEnergyGoal
from apps.test_helpers import test_utils


class EnergyFunctionalTestCase(TransactionTestCase):
    """Energy Test"""
    fixtures = ["base_teams.json"]

    def setUp(self):
        """Initialize a user and log them in."""
        self.user = User.objects.create_user("user", "user@test.com", password="changeme")
        self.team = Team.objects.all()[0]
        profile = self.user.get_profile()
        profile.team = self.team
        profile.setup_complete = True
        profile.setup_profile = True
        profile.save()

        test_utils.register_page_widget("energy", "energy_scoreboard")
        self.client.login(username="user", password="changeme")

    def testIndex(self):
        """Check that we can load the index page."""
        response = self.client.get(reverse("energy_index"))
        self.failUnlessEqual(response.status_code, 200)

    def testEnergyScoreboard(self):
        """test Energy scoreboard."""
        response = self.client.get(reverse("energy_index"))
        goals = response.context["view_objects"]["energy_scoreboard"]["goals_scoreboard"]
        for goal in goals:
            self.assertEqual(goal["completions"], 0, "No team should have completed a goal.")

        goal = TeamEnergyGoal.objects.create(
            team=self.team,
            goal_usage="1",
            actual_usage="2",
        )

        response = self.client.get(reverse("energy_index"))
        goals = response.context["view_objects"]["energy_scoreboard"]["goals_scoreboard"]
        for goal in goals:
            self.assertEqual(goal["completions"], 0, "No team should have completed a goal.")

        goal = TeamEnergyGoal.objects.create(
            team=self.team,
            goal_usage="2",
            actual_usage="1",
        )

        response = self.client.get(reverse("energy_index"))
        goals = response.context["view_objects"]["energy_scoreboard"]["goals_scoreboard"]
        for team in goals:
            if team["team__name"] == self.team.name:
                # print team.teamenergygoal_set.all()
                self.assertEqual(team["completions"], 1,
                    "User's team should have completed 1 goal, but completed %d" % team[
                                                                                    "completions"])
            else:
                self.assertEqual(team["completions"], 0, "No team should have completed a goal.")
