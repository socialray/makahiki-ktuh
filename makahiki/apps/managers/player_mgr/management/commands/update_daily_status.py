"""Invocation:  python manage.py update_energy_usage

For each team, queries WattDepot server to find out cumulative energy usage from
midnight to now. Used for updating the status of the Energy Goal Game."""

import datetime
from apps.managers.player_mgr.models import DailyStatus, Profile
from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand


class Command(MakahikiBaseCommand):
    """command"""
    help = 'Update the number of daily users.'

    def handle(self, *args, **options):
        """Update the number of users that logged in today."""
        print '****** Processing todays users.*******\n'

        today = datetime.datetime.today()
        count = Profile.objects.all().filter(last_visit_date__gte=today,
            last_visit_date__lt=today + datetime.timedelta(days=1)).count()
        print '****** %s visitor(s) today!.*******\n' % count
        state = DailyStatus(date=today, daily_visitors=count)
        state.save()
