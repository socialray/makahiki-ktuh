"""
Settings Manager package
"""

import datetime
from django.conf import settings


def get_round_info():
    """Returns a dictionary containing round information."""
    # Copy the round info and insert the overall round.
    rounds = settings.COMPETITION_ROUNDS.copy()

    #if "Overall" not in rounds:
    #    rounds["Overall"] = {"start": settings.COMPETITION_START,
    #                         "end": settings.COMPETITION_END}

    return rounds


def get_current_round():
    """Get the current round name."""
    round_info = get_current_round_info()
    if round_info is not None:
        return round_info["name"]
    else:
        return None


def get_current_round_info():
    """Gets the current round and associated dates."""
    rounds = get_round_info()
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
