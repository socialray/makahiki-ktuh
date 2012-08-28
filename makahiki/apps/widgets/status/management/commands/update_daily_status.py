"""Invocation:  python manage.py update_energy_usage

For each team, queries WattDepot server to find out cumulative energy usage from
midnight to now. Used for updating the status of the Energy Goal Game."""

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

        count = Profile.objects.filter(last_visit_date=today.date()).count()
        print '****** %s visitor(s) today!.*******\n' % count

        # increase the daily total visitor count
        entry, _ = DailyStatus.objects.get_or_create(date=today.isoformat())
        entry.daily_visitors = count
        entry.save()
