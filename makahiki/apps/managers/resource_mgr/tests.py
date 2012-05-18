"""Energy scoreboard Test"""
import datetime

from django.test import TransactionTestCase
from apps.managers.resource_mgr import resource_mgr
from apps.managers.resource_mgr.models import EnergyUsage
from apps.test_helpers import test_utils


class ResourceManagerTestCase(TransactionTestCase):
    """ResourceManager Test"""

    def setUp(self):
        """Initialize a user and log them in."""
        self.user = test_utils.setup_user("user", "changeme")
        test_utils.set_competition_round()
        self.team = self.user.get_profile().team

    def testEnergy(self):
        """test Energy."""
        date = datetime.date.today()
        _ = EnergyUsage.objects.create(
            team=self.team,
            date=date,
            time=datetime.time(hour=15),
            usage=100,
        )

        rank = resource_mgr.energy_team_rank_info(self.team)["rank"]
        usage = resource_mgr.team_resource_usage(date=date, team=self.team, resource="energy")
        self.assertEqual(rank, 1, "The team should be first rank.")
        self.assertEqual(usage, 100, "The team usage is not correct.")
