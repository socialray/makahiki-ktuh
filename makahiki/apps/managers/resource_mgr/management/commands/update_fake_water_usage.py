"""Invocation:  python manage.py update_fake_water_usage

For each team, update the water usage with fake data. Because water usage input is manual,
this script should only be called once a day in the time specified in the manual_entry_time
of the ResourceGoalSetting."""

import datetime

from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand
from apps.managers.resource_mgr import resource_mgr


class Command(MakahikiBaseCommand):
    """command"""
    help = 'Update the fake water usage for all teams.'

    def handle(self, *args, **options):
        """Update the fake water usage for all teams"""
        date = datetime.datetime.today()
        print '****** Processing fake water usage update at %s *******\n' % date
        resource_mgr.update_fake_water_usage(date)
