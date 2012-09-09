"""module for status collection and analysis."""
from apps.managers.player_mgr.models import Profile
from apps.widgets.status.models import DailyStatus
import datetime


def update_daily_status():
    """update the daily user stats."""
    today = datetime.datetime.today()
    date = today.date()

    # if it is run on mid night, we should count previous day's data
    if today.hour == 0:
        date -= datetime.timedelta(days=1)
    count = Profile.objects.filter(last_visit_date=date).count()
    total = Profile.objects.filter(setup_profile=True).count()

    print '*** daily visitors: %d, total: %d at %s\n' % (count, total, today)

    # update the daily total visitor count, and total setup user count
    entry, _ = DailyStatus.objects.get_or_create(short_date=date)
    entry.daily_visitors = count
    entry.setup_users = total

    entry.save()
