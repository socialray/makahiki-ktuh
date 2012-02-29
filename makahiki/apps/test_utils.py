import datetime
from django.conf import settings


class TestUtils:
    @staticmethod
    def set_competition_round():
        start = datetime.datetime.today() - datetime.timedelta(days=1)
        end = start + datetime.timedelta(days=7)
        settings.COMPETITION_ROUNDS = {
            "Round 1": {
                "start": start,
                "end": end,
                },
            }
