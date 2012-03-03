"""Test for possible quest conditions."""

import datetime
import os

from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.images import ImageFile
from django.db.models import signals

from apps.lib.brabeion import badges
from apps.widgets.quests import possibly_completed_quests, get_quests, has_task, completed_task, \
                                num_tasks_completed, badge_awarded, has_points, set_profile_pic

from apps.widgets.smartgrid.models import Activity, ActivityMember, Commitment, CommitmentMember, \
                                          Category
from apps.lib.avatar import create_default_thumbnails
from apps.lib.avatar.models import Avatar, avatar_file_path
from apps.widgets.raffle.models import RafflePrize, RaffleTicket
from apps.test_utils import TestUtils


class QuestConditionsTest(TestCase):
    """
    Tests for the possible quest conditions.
    """

    def setUp(self):
        self.user = User(username="testuser", password="password")
        self.user.save()

        self.quest = TestUtils.create_quest(completion_conditions=False)

    def testAllocatedTicket(self):
        """
        Test that allocated_ticket works.
        """
        # Create a raffle prize.
        prize = RafflePrize(
            title="Super prize!",
            description="A test prize",
            round_name="Round 1",
            value=5,
        )
        prize.save()

        # Test within context of a quest
        self.quest.unlock_conditions = "allocated_ticket()"
        self.quest.save()
        quests = get_quests(self.user)
        self.assertTrue(self.quest not in quests["available_quests"],
            "User should not be able to participate in this quest.")

        self.quest.unlock_conditions = "not allocated_ticket()"
        self.quest.completion_conditions = "allocated_ticket()"
        self.quest.save()
        quests = get_quests(self.user)
        self.assertTrue(self.quest in quests["available_quests"],
            "User should be able to participate in this quest.")
        self.quest.accept(self.user)

        # Add a raffle ticket and test that the user completed the quest.
        ticket = RaffleTicket(raffle_prize=prize, user=self.user)
        ticket.save()
        completed_quests = possibly_completed_quests(self.user)
        self.assertTrue(self.quest in completed_quests, "User should have completed the quest.")

    def testNumTasksCompleted(self):
        """Test that completing an activity works with num_tasks_completed and has_task."""
        category = Category(name="Test category")
        category.save()
        activity = Activity(
            type="activity",
            name="Test",
            title="Test activity",
            description="Variable points!",
            duration=10,
            point_value=10,
            pub_date=datetime.datetime.today(),
            expire_date=datetime.datetime.today() + datetime.timedelta(days=7),
            confirm_type="text",
            category=category,
        )
        activity.save()

        # Test activities
        member = ActivityMember(user=self.user, activity=activity, approval_status="pending")
        member.save()
        self.assertFalse(num_tasks_completed(self.user, 1, category_name=category.name),
            "User with pending activity should not have completed a task.")
        self.assertFalse(num_tasks_completed(self.user, 1),
            "User with pending activity should not have completed a task.")

        # Test within context of a quest
        self.quest.unlock_conditions = "num_tasks_completed(1, category_name='Test category')"
        self.quest.save()
        quests = get_quests(self.user)
        self.assertTrue(self.quest not in quests,
            "User should not be able to participate in this quest.")

        self.quest.unlock_conditions = "num_tasks_completed(1)"
        self.quest.save()
        quests = get_quests(self.user)
        self.assertTrue(self.quest not in quests,
            "User should not be able to participate in this quest.")

        # Check that the user can now add the quest.
        member.approval_status = "approved"
        member.save()
        quests = get_quests(self.user)
        self.assertTrue(self.quest in quests["available_quests"],
            "User should be able to participate in this quest.")

        self.quest.unlock_conditions = "num_tasks_completed(1, category_name='Test category')"
        self.quest.save()
        quests = get_quests(self.user)
        self.assertTrue(self.quest in quests["available_quests"],
            "User should not be able to participate in this quest.")

        # Test as a completion condition.
        self.quest.accept(self.user)
        self.quest.completion_conditions = "num_tasks_completed(2, category_name='Test category')"
        self.quest.save()
        completed_quests = possibly_completed_quests(self.user)
        self.assertTrue(self.quest not in completed_quests,
            "User should not be able to complete the quest.")

        self.quest.completion_conditions = "num_tasks_completed(2)"
        self.quest.save()
        completed_quests = possibly_completed_quests(self.user)
        self.assertTrue(self.quest not in completed_quests,
            "User should not be able to complete the quest.")

        self.quest.completion_conditions = "num_tasks_completed(1, category_name='Test category')"
        self.quest.save()
        completed_quests = possibly_completed_quests(self.user)
        self.assertTrue(self.quest in completed_quests, "User should have completed the quest.")

    def testNumTasksCompletedWithType(self):
        """test task completed."""
        activity = Activity(
            type="activity",
            name="Test",
            title="Test activity",
            description="Variable points!",
            duration=10,
            point_value=10,
            pub_date=datetime.datetime.today(),
            expire_date=datetime.datetime.today() + datetime.timedelta(days=7),
            confirm_type="text",
        )
        activity.save()

        # Test activities
        member = ActivityMember(user=self.user, activity=activity, approval_status="pending")
        member.save()
        self.assertFalse(num_tasks_completed(self.user, 1, task_type="activity"),
            "User with pending activity should not have completed a task.")

        # Test within context of a quest
        self.quest.unlock_conditions = "num_tasks_completed(1, task_type='activity')"
        self.quest.save()
        quests = get_quests(self.user)
        self.assertTrue(self.quest not in quests,
            "User should not be able to participate in this quest.")

        # Check that the user can now add the quest.
        member.approval_status = "approved"
        member.save()
        quests = get_quests(self.user)
        self.assertTrue(self.quest in quests["available_quests"],
            "User should be able to participate in this quest.")

        # Test as a completion condition.
        self.quest.accept(self.user)
        self.quest.completion_conditions = "num_tasks_completed(2, task_type='activity')"
        self.quest.save()
        completed_quests = possibly_completed_quests(self.user)
        self.assertTrue(self.quest not in completed_quests,
            "User should not be able to complete the quest.")

        self.quest.completion_conditions = "num_tasks_completed(1, task_type='activity')"
        self.quest.save()
        completed_quests = possibly_completed_quests(self.user)
        self.assertTrue(self.quest in completed_quests, "User should have completed the quest.")

    def testHasActivity(self):
        """Test that completing an activity works with has_task."""
        activity = Activity(
            type="activity",
            name="Test",
            slug="test-activity",
            title="Test activity",
            description="Variable points!",
            duration=10,
            point_value=10,
            pub_date=datetime.datetime.today(),
            expire_date=datetime.datetime.today() + datetime.timedelta(days=7),
            confirm_type="text",
        )
        activity.save()

        # Test within context of a quest
        self.quest.unlock_conditions = "has_task(slug='test-activity')"
        self.quest.save()
        quests = get_quests(self.user)
        self.assertTrue(self.quest not in quests,
            "User should not be able to participate in this quest.")

        member = ActivityMember(user=self.user, activity=activity, approval_status="pending")
        member.save()
        self.assertTrue(has_task(self.user, slug="test-activity"),
            "User should have a pending task.")
        self.assertTrue(has_task(self.user, task_type="activity"),
            "User should have a pending task.")

        quests = get_quests(self.user)
        self.assertTrue(self.quest in quests["available_quests"],
            "User should be able to participate in this quest.")

        self.quest.unlock_conditions = "has_task(task_type='activity')"
        self.quest.save()
        quests = get_quests(self.user)
        self.assertTrue(self.quest in quests["available_quests"],
            "User should be able to participate in this quest.")

        member.approval_status = "approved"
        member.save()
        self.assertTrue(has_task(self.user, slug='test-activity'),
            "User should have a completed task.")
        self.assertTrue(has_task(self.user, task_type="activity"),
            "User should have a completed task.")

        # Test as a completion condition.
        self.quest.accept(self.user)
        self.quest.completion_conditions = "not has_task(slug='test-activity')"
        self.quest.save()
        completed_quests = possibly_completed_quests(self.user)
        self.assertTrue(self.quest not in completed_quests,
            "User should not be able to complete the quest.")

        self.quest.completion_conditions = "not has_task(task_type='activity')"
        self.quest.save()
        completed_quests = possibly_completed_quests(self.user)
        self.assertTrue(self.quest not in completed_quests,
            "User should not be able to complete the quest.")

        self.quest.completion_conditions = "has_task(slug='test-activity')"
        self.quest.save()
        completed_quests = possibly_completed_quests(self.user)
        self.assertTrue(self.quest in completed_quests, "User should have completed the quest.")

    def testCompletedActivity(self):
        """Tests that completed_task works when a task is completed."""
        activity = Activity(
            type="activity",
            name="Test",
            title="Test activity",
            slug="test-activity",
            description="Variable points!",
            duration=10,
            point_value=10,
            pub_date=datetime.datetime.today(),
            expire_date=datetime.datetime.today() + datetime.timedelta(days=7),
            confirm_type="text",
        )
        activity.save()

        # Test within context of a quest
        self.quest.unlock_conditions = "completed_task(slug='test-activity')"
        self.quest.save()
        quests = get_quests(self.user)
        self.assertTrue(self.quest not in quests,
            "User should not be able to participate in this quest.")

        member = ActivityMember(user=self.user, activity=activity, approval_status="approved")
        member.save()
        self.assertTrue(completed_task(self.user, slug="test-activity"),
            "User should have completed 'Test'.")
        self.assertTrue(completed_task(self.user, task_type="activity"),
            "User should have completed an activity")

        quests = get_quests(self.user)
        self.assertTrue(self.quest in quests["available_quests"],
            "User should be able to participate in this quest.")

        self.quest.unlock_conditions = "completed_task(task_type='activity')"
        self.quest.save()
        quests = get_quests(self.user)
        self.assertTrue(self.quest in quests["available_quests"],
            "User should be able to participate in this quest.")

        # Test as a completion condition.
        self.quest.accept(self.user)
        self.quest.completion_conditions = "not completed_task(slug='test-activity')"
        self.quest.save()
        completed_quests = possibly_completed_quests(self.user)
        self.assertTrue(self.quest not in completed_quests,
            "User should not be able to complete the quest.")

        self.quest.completion_conditions = "not completed_task(task_type='activity')"
        self.quest.save()
        completed_quests = possibly_completed_quests(self.user)
        self.assertTrue(self.quest not in completed_quests,
            "User should not be able to complete the quest.")

        self.quest.completion_conditions = "completed_task(slug='test-activity')"
        self.quest.save()
        completed_quests = possibly_completed_quests(self.user)
        self.assertTrue(self.quest in completed_quests, "User should have completed the quest.")

    def testCommitmentsNumCompleted(self):
        """Tests that num_tasks_completed works for a completed commitment."""
        commitment = Commitment(
            title="Test commitment",
            type="commitment",
            name="Test",
            description="A commitment!",
            point_value=10,
        )
        commitment.save()

        member = CommitmentMember(user=self.user, commitment=commitment)
        member.save()
        self.assertFalse(num_tasks_completed(self.user, 1),
            "User with commitment in progress should not have completed a task.")

        # Test as an unlock condition
        self.quest.unlock_conditions = "num_tasks_completed(1)"
        self.quest.save()
        self.assertTrue(self.quest not in get_quests(self.user),
            "User should not be able to participate in this quest.")

        member.award_date = datetime.datetime.today()
        member.save()
        self.assertTrue(num_tasks_completed(self.user, 1),
            "User that has a completed commitment did not complete a task.")
        self.assertTrue(self.quest in get_quests(self.user)["available_quests"],
            "User should be able to participate in this quest.")

        # Test as a completion condition
        self.quest.accept(self.user)
        self.quest.completion_conditions = "num_tasks_completed(2)"
        self.quest.save()
        self.assertTrue(self.quest not in possibly_completed_quests(self.user),
            "User should not be able to complete this quest.")

        self.quest.completion_conditions = "num_tasks_completed(1)"
        self.quest.save()
        self.assertTrue(self.quest in possibly_completed_quests(self.user),
            "User should be able to complete this quest.")

    def testHasCommitment(self):
        """Tests that has_task works for a commitment in progress."""
        commitment = Commitment(
            title="Test commitment",
            type="commitment",
            name="Test",
            slug="test-commitment",
            description="A commitment!",
            point_value=10,
        )
        commitment.save()

        # Test as an unlock condition.
        self.quest.unlock_conditions = "has_task(slug='test-commitment')"
        self.quest.save()
        self.assertTrue(self.quest not in get_quests(self.user),
            "User should not be able to participate in this quest.")

        member = CommitmentMember(user=self.user, commitment=commitment)
        member.save()
        self.assertTrue(has_task(self.user, slug='test-commitment'),
            "User should have a commitment in progress.")
        self.assertTrue(has_task(self.user, task_type="commitment"),
            "User should have a commitment in progress.")

        self.assertTrue(self.quest in get_quests(self.user)["available_quests"],
            "User should be able to participate in this quest.")
        self.quest.unlock_conditions = "has_task(task_type='commitment')"
        self.quest.save()
        self.assertTrue(self.quest in get_quests(self.user)["available_quests"],
            "User should be able to participate in this quest.")

        member.award_date = datetime.datetime.today()
        member.save()
        self.assertTrue(has_task(self.user, slug='test-commitment'),
            "User should have a completed commitment.")
        self.assertTrue(has_task(self.user, task_type="commitment"),
            "User should have a completed commitment.")

        # Test as a completion condition
        self.quest.accept(self.user)
        self.quest.completion_conditions = "not has_task(slug='test-commitment')"
        self.quest.save()
        self.assertTrue(self.quest not in possibly_completed_quests(self.user),
            "User should not be able to complete this quest.")

        self.quest.completion_conditions = "not has_task(task_type='commitment')"
        self.quest.save()
        self.assertTrue(self.quest not in possibly_completed_quests(self.user),
            "User should not be able to complete this quest.")

        self.quest.completion_conditions = "has_task(slug='test-commitment')"
        self.quest.save()
        self.assertTrue(self.quest in possibly_completed_quests(self.user),
            "User should be able to complete this quest.")

    def testBadgeAwarded(self):
        """Tests that badge awarded works for a user."""
        from apps.widgets.badges.user_badges import DailyVisitorBadge

        badges.register(DailyVisitorBadge)

        profile = self.user.get_profile()
        self.assertFalse(badge_awarded(self.user, "dailyvisitor"),
            "New user should not be awarded the daily visitor badge.")

        # Test as a quest unlock condition.
        self.quest.unlock_conditions = "badge_awarded('dailyvisitor')"
        self.quest.save()
        self.assertTrue(self.quest not in get_quests(self.user),
            "User should not be able to participate in this quest.")

        self.quest.unlock_conditions = "not badge_awarded('dailyvisitor')"
        self.quest.save()
        self.assertTrue(self.quest in get_quests(self.user)["available_quests"],
            "User should be able to participate in this quest.")

        self.quest.accept(self.user)
        self.quest.completion_conditions = "badge_awarded('dailyvisitor')"
        self.quest.save()
        self.assertTrue(self.quest not in possibly_completed_quests(self.user),
            "User should not be able to complete this quest.")

        profile.daily_visit_count = 3
        profile.save()
        badges.possibly_award_badge("dailyvisitor", user=self.user)
        self.assertTrue(badge_awarded(self.user, "dailyvisitor"),
            "User should have been awarded the daily visitor badge.")
        self.assertTrue(self.quest in possibly_completed_quests(self.user),
            "User should have completed this quest.")

    def testHasPointsOverall(self):
        """Tests that has_points works for a user."""
        profile = self.user.get_profile()
        test_points = 10
        self.assertFalse(has_points(self.user, test_points), "User should not have any points")
        profile.points = test_points
        profile.save()
        self.assertTrue(has_points(self.user, test_points), "User should have enough points.")

        # Test within context of a quest.
        profile.points = 0
        profile.save()
        self.quest.unlock_conditions = "has_points(10)"
        self.quest.save()
        self.assertTrue(self.quest not in get_quests(self.user),
            "User should not be able to participate in this quest.")

        self.quest.unlock_conditions = "not has_points(10)"
        self.quest.save()
        print self.user.get_profile().points
        self.assertTrue(self.quest in get_quests(self.user)["available_quests"],
            "User should be able to participate in this quest.")

        self.quest.accept(self.user)
        self.quest.completion_conditions = "has_points(10)"
        self.quest.save()
        self.assertTrue(self.quest not in possibly_completed_quests(self.user),
            "User should not be able to complete this quest.")

        profile.points = 10
        profile.save()
        self.assertTrue(self.quest in possibly_completed_quests(self.user),
            "User should have completed this quest.")

    def testPostedToWall(self):
        """
        Tests that this predicate is completed when the user posts something to their wall.
        """
        from apps.managers.team_mgr.models import Group, Team, Post
        from apps.widgets.quests import posted_to_wall

        group = Group.objects.create(name="test", slug="test")
        team = Team.objects.create(name="a", slug="a", group=group)
        profile = self.user.get_profile()
        profile.team = team
        profile.save()

        self.assertFalse(posted_to_wall(self.user), "User should not have posted to their wall.")
        post = Post.objects.create(user=self.user, team=team, text="text")
        self.assertTrue(posted_to_wall(self.user), "User should have posted to their own wall.")

        # Test within context of a quest.
        post.delete()
        self.quest.unlock_conditions = "posted_to_wall()"
        self.quest.save()
        self.assertTrue(self.quest not in get_quests(self.user),
            "User should not be able to participate in this quest.")

        self.quest.unlock_conditions = "not posted_to_wall()"
        self.quest.save()
        self.assertTrue(self.quest in get_quests(self.user)["available_quests"],
            "User should be able to participate in this quest.")

        self.quest.accept(self.user)
        self.quest.completion_conditions = "posted_to_wall()"
        self.quest.save()
        self.assertTrue(self.quest not in possibly_completed_quests(self.user),
            "User should not be able to complete this quest.")

        post = Post.objects.create(user=self.user, team=team, text="text")
        self.assertTrue(self.quest in possibly_completed_quests(self.user),
            "User should have completed this quest.")

    def testSetProfilePic(self):
        """
        Tests that this predicate is completed when the user sets a profile pic.
        """
        # Need to disconnect create thumbnail signal temporarily for test so that additional image
        # files don't get created.
        signals.post_save.disconnect(create_default_thumbnails, Avatar)

        self.assertFalse(set_profile_pic(self.user), "User should not have their profile pic set.")
        image_path = os.path.join(settings.PROJECT_ROOT, "fixtures", "test_images", "test.jpg")
        image = ImageFile(open(image_path, "r"))
        path = avatar_file_path(user=self.user, filename="test.jpg")
        avatar = Avatar(user=self.user, avatar=path, primary=True)
        avatar.avatar.storage.save(path, image)
        avatar.save()
        self.assertTrue(set_profile_pic(self.user), "User should have their profile pic set.")

        # Test within context of a quest.
        avatar.delete()
        self.quest.unlock_conditions = "set_profile_pic()"
        self.quest.save()
        self.assertTrue(self.quest not in get_quests(self.user),
            "User should not be able to participate in this quest.")

        self.quest.unlock_conditions = "not set_profile_pic()"
        self.quest.save()
        self.assertTrue(self.quest in get_quests(self.user)["available_quests"],
            "User should be able to participate in this quest.")

        self.quest.accept(self.user)
        self.quest.completion_conditions = "set_profile_pic()"
        self.quest.save()
        self.assertTrue(self.quest not in possibly_completed_quests(self.user),
            "User should not be able to complete this quest.")

        avatar = Avatar(user=self.user, avatar=path, primary=True)
        avatar.save()
        self.assertTrue(self.quest in possibly_completed_quests(self.user),
            "User should have completed this quest.")

        # Be sure to clean up test files and reconnect post_save signal.
        signals.post_save.connect(create_default_thumbnails, sender=Avatar)
        for avatar in self.user.avatar_set.all():
            avatar.avatar.delete()
            avatar.delete()
