"""Test Unitilities"""
import datetime
from django.conf import settings
from apps.managers.settings_mgr.models import PageSettings


class TestUtils:
    """Test Utilities"""
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
