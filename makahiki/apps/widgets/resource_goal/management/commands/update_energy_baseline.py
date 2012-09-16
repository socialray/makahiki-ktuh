"""Invocation:  python manage.py update_energy_baseline

update the daily baseline."""

import datetime

from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand
from apps.widgets.resource_goal import resource_goal


class Command(MakahikiBaseCommand):
    """command"""
    help = 'Update daily baseline for all teams'

    def handle(self, *args, **options):
        """update the daily baseline"""
        today = datetime.datetime.today()
        print '****** Processing update_energy_baseline for %s *******\n' % today

        today = today.date()
        # update the baseline
        resource_goal.update_resource_baseline("energy", today, 2)
