"""Handles request for prize status."""

from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.score_mgr.models import ScoreboardEntry
from apps.widgets.raffle.models import RafflePrize


def supply(request, page_name):
    """supply view_objects for prize status."""
    _ = page_name
    _ = request

    # get the raffle_prizes for all rounds
    raffle_prizes = {}
    for round_name in challenge_mgr.get_all_round_info():
        raffle_prizes[round_name] = RafflePrize.objects.filter(round_name=round_name).all()

    # Calculate unused raffle tickets for every user.
    round_name = challenge_mgr.get_round_name()
    elig_entries = ScoreboardEntry.objects.filter(
        points__gte=25,
        round_name=round_name)
    unused = 0
    errors = []
    for entry in elig_entries:
        available = (entry.points / 25) - entry.profile.user.raffleticket_set.count()
        if available < 0:
            errors.append(entry.profile)
        unused += available

    return {
        "raffle_prizes": raffle_prizes,
        "unused": unused,
        "has_error": len(errors) > 0,
        "errors": errors,
        }
