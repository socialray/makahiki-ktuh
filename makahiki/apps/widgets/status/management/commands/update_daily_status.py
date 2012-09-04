"""Invocation:  python manage.py update_daily_status

Update the number of users that logged in today.
"""

import datetime
from apps.managers.player_mgr.models import Profile
from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand
from apps.widgets.status.models import DailyStatus


class Command(MakahikiBaseCommand):
    """command"""
    help = 'Update the number of daily users.'

    def handle(self, *args, **options):
        """Update the number of users that logged in today."""
        today = datetime.datetime.today()
        print '****** Processing daily user count update at %s.*******\n' % today

        date = today.date()

        # if it is run on mid night, we should count previous day's data
        if today.hour == 0:
            date -= datetime.timedelta(days=1)
        count = Profile.objects.filter(last_visit_date=date).count()

        date_string = "%s" % date

        print '****** %s visitor(s) for %s *******\n' % (count, date_string)

        # increase the daily total visitor count
        entry, _ = DailyStatus.objects.get_or_create(date=date_string)
        entry.daily_visitors = count
        entry.save()
