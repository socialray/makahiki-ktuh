"""Handles request for prize status."""

from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.score_mgr.models import ScoreboardEntry
from apps.widgets.raffle.models import RafflePrize
import operator


def supply(request, page_name):
    """supply view_objects for prize status."""
    _ = page_name
    _ = request

    # get the raffle_prizes for all rounds
    raffle_prizes = {}
    for round_name in challenge_mgr.get_all_round_info()["rounds"]:
        raffle_prizes[round_name] = RafflePrize.objects.filter(round_name=round_name).all()

    # Calculate unused raffle tickets for every user.
    elig_entries = ScoreboardEntry.objects.filter(
        points__gte=25,
        round_name=challenge_mgr.get_round_name())

    unused = 0
    errors = []
    for entry in elig_entries:
        available = (entry.points / 25) - entry.profile.user.raffleticket_set.count()
        if available < 0:
            errors.append(entry.profile)
        unused += available

    # get user/ticket pairings
    unused_tickets = {}
    temp = {}
    for item in ScoreboardEntry.objects.all():
        if(item.profile.id in temp):
            temp[item.profile.id] = (item.profile, temp[item.profile.id][1] + item.points)
        else:
            temp[item.profile.id] = (item.profile, item.points)

    for item, key in temp.iteritems():
        unused_tickets[key[0]] = key[1] / 25 - key[0].user.raffleticket_set.count()

    sorted_list = sorted(unused_tickets.iteritems(), key=operator.itemgetter(1))
    sorted_list.reverse()

    return {
        "raffle_prizes": raffle_prizes,
        "unused": unused,
        "unused_tickets": sorted_list,
        "has_error": len(errors) > 0,
        "errors": errors,
        }
