"""
test point transaction log
"""

import datetime

from django.test import TestCase
from django.contrib.auth.models import User

from managers.player_mgr.models import PointsTransaction

class PointsLogTest(TestCase):
    """test points log"""
    def setUp(self):
        self.user = User.objects.create_user("test", "test@test.com")

    def testAddPoints(self):
        """
        Test that adding points creates a new entry in the points log.
        """
        log_count = PointsTransaction.objects.count()
        profile = self.user.get_profile()
        profile.add_points(10, datetime.datetime.today(), "Hello world", None)
        profile.save()

        self.assertEqual(PointsTransaction.objects.count(), log_count + 1,
            "A new log should have been created.")
        log = profile.user.pointstransaction_set.all()[0]
        self.assertEqual(log.points, 10, "Points should have been awarded.")
        self.assertEqual(log.message, "Hello world",
            "Message should have been added.")
