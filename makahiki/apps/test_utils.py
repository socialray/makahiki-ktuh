"""Test Unitilities"""
import datetime
from django.conf import settings
from django.contrib.auth.models import User
from apps.managers.settings_mgr.models import PageSettings
from apps.managers.team_mgr.models import Team


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
    def register_page_widget(page_name, widget_name):
        """Register a widget with a page."""
        PageSettings(name=page_name, widget=widget_name).save()

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
