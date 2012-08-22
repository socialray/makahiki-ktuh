"""handles request for user status."""
import datetime
from django.contrib.auth.models import User
from django.db.models import Min
from django.db.models.aggregates import Count
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.player_mgr.models import Profile


def supply(request, page_name):
    """supply view_objects for user status."""
    _ = page_name
    _ = request

    todays_users = Profile.objects.filter(last_visit_date=datetime.datetime.today())

    # Approximate logins by their first points transaction.
    rounds_info = challenge_mgr.get_all_round_info()
    start = rounds_info["competition_start"]
    today = datetime.datetime.today()

    users_anno = User.objects.annotate(login_date=Min('pointstransaction__transaction_date'))
    logins = []
    while start <= today:
        result = {}
        result['date'] = start.strftime("%m/%d")

        result['logins'] = users_anno.filter(login_date__gte=start,
            login_date__lt=start + datetime.timedelta(days=1)).count()
        logins.append(result)
        start += datetime.timedelta(days=1)

    # Find referrals.
    referrals = Profile.objects.filter(referring_user__isnull=False).values(
        'referring_user__profile__name', 'referring_user__username').annotate(
            referrals=Count('referring_user')
    )

    return {
        "todays_users": todays_users,
        'logins': logins,
        "referrals": referrals,
        }


def remote_supply(request, page_name):
    """Supports remote calls to this view."""
    return supply(request, page_name)
