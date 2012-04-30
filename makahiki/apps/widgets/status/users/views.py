"""handles request for user status."""
import datetime

from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Min
from apps.managers.player_mgr.models import Profile


def supply(request, page_name):
    """supply view_objects for user status."""
    _ = page_name
    _ = request

    todays_users = Profile.objects.filter(last_visit_date=datetime.datetime.today())

    # Approximate logins by their first points transaction.
    start = settings.COMPETITION_START
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

    return {
        "todays_users": todays_users,
        'logins': logins,
        }
