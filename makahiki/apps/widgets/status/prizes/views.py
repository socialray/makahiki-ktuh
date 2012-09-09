"""Handles request for prize status."""
from django.db.models import Count

from apps.managers.challenge_mgr import challenge_mgr
from apps.widgets.raffle.models import RafflePrize


def supply(request, page_name):
    """supply view_objects for prize status."""
    _ = page_name
    _ = request

    # get the raffle_prizes for all rounds
    raffle_prizes = {}
    current_round = challenge_mgr.get_round_name()
    rounds = challenge_mgr.get_all_round_info()["rounds"]
    for key in rounds.keys():
        if key <= current_round:
            raffle_prizes[key] = RafflePrize.objects.filter(
                round_name=key).annotate(count=Count('raffleticket')).order_by('-count')

    return {
        "raffle_prizes": raffle_prizes,
        }
