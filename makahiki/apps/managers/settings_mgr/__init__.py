"""
Settings Manager package
"""

import datetime
from django.conf import settings


def get_current_round():
    """Get the current round name."""
    return get_current_round_info()["name"]


def get_current_round_info():
    """Gets the current round and associated dates."""
    rounds = settings.COMPETITION_ROUNDS
    today = datetime.datetime.today()
    for key in rounds.keys():
        start = rounds[key]["start"]
        end = rounds[key]["end"]
        if today >= start and today < end:
            return {
                "name": key,
                "start": start,
                "end": end,
                }

    # No current round.
    return None


def in_competition():
    """Returns true if we are still in the competition."""
    today = datetime.datetime.today()
    return settings.COMPETITION_START < today and today < settings.COMPETITION_END
