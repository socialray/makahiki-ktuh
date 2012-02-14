import os
import datetime

from django.test import TestCase
from django.conf import settings
from django.core.files.images import ImageFile
from django.contrib.auth.models import User

from widgets.prizes.models import Prize
from managers.team_mgr.models import Dorm, Team

class DormTeamPrizeTests(TestCase):
    """
    Tests awarding a prize to a dorm team points winner.
    """

    def setUp(self):
        """
        Sets up a test individual prize for the rest of the tests.
        This prize is not saved, as the round field is not yet set.
        """
        image_path = os.path.join(settings.PROJECT_ROOT, "fixtures", "test_images", "test.jpg")
        image = ImageFile(open(image_path, "r"))
        self.prize = Prize(
            title="Super prize!",
            short_description="A test prize",
            long_description="A test prize",
            image=image,
            award_to="team_dorm",
            competition_type="points",
            value=5,
        )

        self.saved_rounds = settings.COMPETITION_ROUNDS
        self.current_round = "Round 1"
        start = datetime.date.today()
        end = start + datetime.timedelta(days=7)

        settings.COMPETITION_ROUNDS = {
            "Round 1": {
                "start": start.strftime("%Y-%m-%d"),
                "end": end.strftime("%Y-%m-%d"),
                },
            }

        # Create test dorms, teams, and users.
        self.dorms = [Dorm(name="Test Dorm %d" % i) for i in range(0, 2)]
        _ = [d.save() for d in self.dorms]

        self.teams = [Team(name=str(i), dorm=self.dorms[i % 2]) for i in range(0, 4)]
        _ = [f.save() for f in self.teams]

        self.users = [User.objects.create_user("test%d" % i, "test@test.com") for i in range(0, 4)]

        # Assign users to teams.
        for index, user in enumerate(self.users):
            user.get_profile().team = self.teams[index % 4]
            user.get_profile().save()

    def testNumAwarded(self):
        """
        Checks that the number of prizes to award for this prize is the same as the number of dorms.
        """
        self.prize.round_name = "Round 1"
        self.prize.save()

        self.assertEqual(self.prize.num_awarded(self.teams[0]), len(self.dorms),
            "One prize should be awarded to each of the dorms in the competition.")

    def testRoundLeader(self):
        """
        Tests that we can retrieve the overall individual points leader for a round prize.
        """
        self.prize.round_name = "Round 1"
        self.prize.save()

        # Test one user will go ahead in points.
        profile = self.users[0].get_profile()
        profile.add_points(10, datetime.datetime.today() - datetime.timedelta(minutes=1), "test")
        profile.save()

        self.assertEqual(self.prize.leader(profile.team), profile.team,
            "The user's team is not leading in the prize.")

        # Test a user in a different dorm.
        profile1 = self.users[1].get_profile()
        profile1.add_points(profile.points + 1,
            datetime.datetime.today() - datetime.timedelta(minutes=1), "test")
        profile1.save()

        self.assertEqual(self.prize.leader(profile.team), profile.team,
            "The leader for this prize in first users dorm should not change.")
        self.assertEqual(self.prize.leader(profile1.team), profile1.team,
            "The leader in profile1's dorm is not profile1.")

        # Test that a user in a different team but same dorm changes the leader for the original user.
        profile2 = self.users[2].get_profile()
        profile2.add_points(profile.points + 1,
            datetime.datetime.today() - datetime.timedelta(minutes=1), "test")
        profile2.save()

        self.assertEqual(self.prize.leader(profile.team), profile2.team,
            "The leader for this prize did not change.")
        self.assertEqual(self.prize.leader(profile1.team), profile1.team,
            "The leader in profile1's dorm is not profile1.")

    def testOverallLeader(self):
        """
        Tests that we can retrieve the overall individual points leader for a round prize.
        """
        self.prize.round = "Overall"
        self.prize.save()

        # Test one user will go ahead in points.
        profile = self.users[0].get_profile()
        profile.add_points(10, datetime.datetime.today() - datetime.timedelta(minutes=1), "test")
        profile.save()

        self.assertEqual(self.prize.leader(profile.team), profile.team,
            "The user's team is not leading in the prize.")

        # Test a user in a different dorm.
        profile1 = self.users[1].get_profile()
        profile1.add_points(profile.points + 1,
            datetime.datetime.today() - datetime.timedelta(minutes=1), "test")
        profile1.save()

        self.assertEqual(self.prize.leader(profile.team), profile.team,
            "The leader for this prize in first users dorm should not change.")
        self.assertEqual(self.prize.leader(profile1.team), profile1.team,
            "The leader in profile1's dorm is not profile1.")

        # Test that a user in a different team but same dorm changes the leader for the original user.
        profile2 = self.users[2].get_profile()
        profile2.add_points(profile.points + 1,
            datetime.datetime.today() - datetime.timedelta(minutes=1), "test")
        profile2.save()

        self.assertEqual(self.prize.leader(profile.team), profile2.team,
            "The leader for this prize did not change.")
        self.assertEqual(self.prize.leader(profile1.team), profile1.team,
            "The leader in profile1's dorm is not profile1.")

    def tearDown(self):
        """
        Deletes the created image file in prizes.
        """
        settings.COMPETITION_ROUNDS = self.saved_rounds
        self.prize.image.delete()
        self.prize.delete()


class OverallTeamPrizeTest(TestCase):
    """
    Tests awarding a prize to a dorm team points winner.
    """

    def setUp(self):
        """
        Sets up a test individual prize for the rest of the tests.
        This prize is not saved, as the round field is not yet set.
        """
        image_path = os.path.join(settings.PROJECT_ROOT, "fixtures", "test_images", "test.jpg")
        image = ImageFile(open(image_path, "r"))
        self.prize = Prize(
            title="Super prize!",
            short_description="A test prize",
            long_description="A test prize",
            image=image,
            award_to="team_overall",
            competition_type="points",
            value=5,
        )

        self.saved_rounds = settings.COMPETITION_ROUNDS
        self.current_round = "Round 1"
        start = datetime.date.today()
        end = start + datetime.timedelta(days=7)

        settings.COMPETITION_ROUNDS = {
            "Round 1": {
                "start": start.strftime("%Y-%m-%d"),
                "end": end.strftime("%Y-%m-%d"),
                },
            }

        # Create test dorms, teams, and users.
        self.dorm = Dorm(name="Test Dorm")
        self.dorm.save()

        self.teams = [Team(name=str(i), dorm=self.dorm) for i in range(0, 2)]
        _ = [f.save() for f in self.teams]

        self.users = [User.objects.create_user("test%d" % i, "test@test.com") for i in range(0, 4)]

        # Assign users to teams.
        for index, user in enumerate(self.users):
            user.get_profile().team = self.teams[index % 2]
            user.get_profile().save()

    def testNumAwarded(self):
        """
        Simple test to check that the number of prizes to be awarded is one.
        """
        self.prize.round_name = "Round 1"
        self.prize.save()

        self.assertEqual(self.prize.num_awarded(), 1,
            "This prize should not be awarded to more than one user.")

    def testRoundLeader(self):
        """
        Tests that we can retrieve the overall individual points leader for a round prize.
        """
        self.prize.round_name = "Round 1"
        self.prize.save()

        # Test one user will go ahead in points.
        profile = self.users[0].get_profile()
        profile.add_points(10, datetime.datetime.today() - datetime.timedelta(minutes=1), "test")
        profile.save()

        self.assertEqual(self.prize.leader(profile.team), profile.team,
            "The user's team is not leading in the prize.")

        # Test that a user in a different team changes the leader for the original user.
        profile2 = self.users[2].get_profile()
        profile2.add_points(profile.points + 1,
            datetime.datetime.today() - datetime.timedelta(minutes=1), "test")
        profile2.save()

        self.assertEqual(self.prize.leader(profile.team), profile2.team,
            "The leader for this prize did not change.")

    def testOverallLeader(self):
        """
        Tests that we can retrieve the overall individual points leader for a round prize.
        """
        self.prize.round = "Overall"
        self.prize.save()

        # Test one user will go ahead in points.
        profile = self.users[0].get_profile()
        profile.add_points(10, datetime.datetime.today() - datetime.timedelta(minutes=1), "test")
        profile.save()

        self.assertEqual(self.prize.leader(profile.team), profile.team,
            "The user's team is not leading in the prize.")

        # Test that a user in a different team but same dorm changes the leader for the original user.
        profile2 = self.users[2].get_profile()
        profile2.add_points(profile.points + 1,
            datetime.datetime.today() - datetime.timedelta(minutes=1), "test")
        profile2.save()

        self.assertEqual(self.prize.leader(profile.team), profile2.team,
            "The leader for this prize did not change.")

    def tearDown(self):
        """
        Deletes the created image file in prizes.
        """
        settings.COMPETITION_ROUNDS = self.saved_rounds
        self.prize.image.delete()
        self.prize.delete()