"""Provide the view of the prizes widget."""
import datetime

from django.template.defaultfilters import slugify

from apps.managers.challenge_mgr import challenge_mgr
from apps.widgets.prizes.models import Prize


def supply(request, page_name):
    """Supply view_object content, which is the prizes for this team."""
    _ = page_name
    team = request.user.get_profile().team
    prizes = _get_prizes(team)

    return {
        "prizes": prizes,
        }


def _get_prizes(team):
    """Private method to process the prizes half of the page.
       Takes the user's team and returns a dictionary to be used in the template."""
    rounds = challenge_mgr.get_round_info()
    prize_dict = {}
    today = datetime.datetime.today()
    for key in rounds.keys():
        prizes = Prize.objects.filter(round_name=key)
        for prize in prizes:
            if key != "Overall" and today < rounds[key]["start"]:
                # If the round happens in the future, we don't care who the leader is.
                prize.current_leader = "TBD"

            elif prize.competition_type == "points":
                # If we are in the middle of the round, display the current leader.
                if today < rounds[key]["end"]:
                    prize.current_leader = prize.leader(team)
                else:
                    prize.winner = prize.leader(team)

            # Else, this is an energy competition prize.
            else:
                # Slugify the round name to create a CSS id.
                prize_id = slugify(key) + "-leader"
                if today < rounds[key]["end"]:
                    prize.current_leader = "<span id='%s'></span>" % prize_id
                else:
                    prize.winner = "<span id='%s'></span>" % prize_id

        prize_dict[key] = prizes

    return prize_dict
