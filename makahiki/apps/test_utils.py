import datetime
from django.conf import settings

class TestUtils:
    @staticmethod
    def set_competition_round():
        start = datetime.date.today()
        end = start + datetime.timedelta(days=7)
        settings.COMPETITION_ROUNDS = {
            "Round 1": {
                "start": start.strftime("%Y-%m-%d %H:%M:%S"),
                "end": end.strftime("%Y-%m-%d %H:%M:%S"),
                },
            }