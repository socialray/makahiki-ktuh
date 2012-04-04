"""Test Unitilities"""
import datetime
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.images import ImageFile
from apps.managers.settings_mgr.models import PageSettings
from apps.managers.team_mgr.models import Team, Group
from apps.widgets.prizes.models import Prize
from apps.widgets.quests.models import Quest


class TestUtils:
    """Test Utilities"""
    @staticmethod
    def setup_user(username, password):
        """setup test user"""
        user = User.objects.create_user(username=username, email=username + "@test.com",
                                        password=password)
        team = Team.objects.all()[0]
        profile = user.get_profile()
        profile.team = team
        profile.setup_complete = True
        profile.setup_profile = True
        profile.save()
        return user

    @staticmethod
    def set_competition_round():
        """set the competition round for test."""
        start = datetime.datetime.today() - datetime.timedelta(days=1)
        end = start + datetime.timedelta(days=7)
        settings.COMPETITION_ROUNDS = {
            "Round 1": {
                "start": start,
                "end": end,
                },
            }

    @staticmethod
    def set_two_rounds():
        """set two rounds for this test"""
        start = datetime.datetime.today() - datetime.timedelta(days=8)
        end1 = start + datetime.timedelta(days=7)
        end2 = start + datetime.timedelta(days=14)
        settings.COMPETITION_ROUNDS = {
            "Round 1": {
                "start": start,
                "end": end1,
                },
            "Round 2": {
                "start": end1,
                "end": end2,
                },
            }
        settings.COMPETITION_START = start
        settings.COMPETITION_END = end2

    @staticmethod
    def register_page_widget(page_name, widget_name):
        """Register a widget with a page."""
        PageSettings.objects.get_or_create(name=page_name, widget=widget_name)

    @staticmethod
    def create_event(slug=None):
        """create test event"""
        from apps.widgets.smartgrid.models import Activity

        if slug is None:
            slug = "test-event"
        event = Activity.objects.create(
            title="Test event",
            slug=slug,
            description="Testing!",
            duration=10,
            point_value=10,
            pub_date=datetime.datetime.today(),
            expire_date=datetime.datetime.today() + datetime.timedelta(days=7),
            confirm_type="code",
            type="event",
            event_date=datetime.datetime.today() + datetime.timedelta(days=1),
            )
        return event

    @staticmethod
    def create_activity():
        """create test activity"""
        from apps.widgets.smartgrid.models import Activity

        return Activity.objects.create(
            title="Test activity",
            description="Testing!",
            slug="test-activity",
            duration=10,
            point_value=10,
            pub_date=datetime.datetime.today(),
            expire_date=datetime.datetime.today() + datetime.timedelta(days=7),
            confirm_type="text",
            type="activity",
        )

    @staticmethod
    def create_teams(testcase):
        """Create test groups, teams, and users."""
        testcase.groups = [Group(name="Test Group %d" % i) for i in range(0, 2)]
        _ = [d.save() for d in testcase.groups]

        testcase.group = Group(name="Test Group")
        testcase.group.save()

        testcase.teams = [Team(name=str(i), group=testcase.group) for i in range(0, 2)]
        _ = [f.save() for f in testcase.teams]
        testcase.users = [User.objects.create_user(
            "test%d" % i, "test@test.com") for i in range(0, 4)]
        # Assign users to teams.
        for index, user in enumerate(testcase.users):
            user.get_profile().team = testcase.teams[index % 2]
            user.get_profile().save()

    @staticmethod
    def setup_prize(award_to, competition_type):
        """set the prize for testing"""
        image_path = os.path.join(settings.PROJECT_ROOT, "fixtures", "test_images", "test.jpg")
        image = ImageFile(open(image_path, "r"))
        prize = Prize(
            title="Super prize!",
            short_description="A test prize",
            long_description="A test prize",
            image=image,
            award_to=award_to,
            competition_type=competition_type,
            value=5,
            )
        prize.save()
        return prize

    @staticmethod
    def create_quest(completion_conditions):
        """create the test quest"""
        quest = Quest(
                name="Test quest",
                quest_slug="test_quest",
                description="test quest",
                level=1,
                unlock_conditions="True",
                completion_conditions=completion_conditions,
                )
        quest.save()
        return quest
