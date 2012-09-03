"""Invocation:  python manage.py update_energy_usage

For each team, queries WattDepot server to find out cumulative energy usage from
midnight to now. Used for updating the status of the Energy Goal Game."""

import datetime

from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand
from apps.managers.resource_mgr import resource_mgr


class Command(MakahikiBaseCommand):
    """command"""
    help = 'Update the energy usage for all teams from wattdepot server.'

    def handle(self, *args, **options):
        """Update the energy usage for all teams."""
        date = datetime.datetime.today()
        print '****** Processing energy usage update at %s *******\n' % date
        resource_mgr.update_energy_usage(date)
