"""Provides predicate functions for runtime condition evaluation."""
from apps.managers.challenge_mgr.models import GameInfo


def game_enabled(user, name):
    """Returns True if the game is enabled."""
    _ = user
    return GameInfo.objects.filter(name=name, enabled=True).count()
