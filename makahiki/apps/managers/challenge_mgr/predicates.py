"""Predicates regarding the state of the challenge."""

import datetime
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.challenge_mgr.models import GameInfo


def game_enabled(user, name):
    """Returns True if the game is enabled."""
    _ = user
    return GameInfo.objects.filter(name=name, enabled=True).count()


def reached_round(user, name):
    """Returns True if the current time was past the start of specified round."""
    _ = user
    info = challenge_mgr.get_round_info(name)
    today = datetime.datetime.today()
    return info and today >= info["start"]
