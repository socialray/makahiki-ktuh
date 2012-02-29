"""Test Unitilities"""
import datetime
from django.conf import settings


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
