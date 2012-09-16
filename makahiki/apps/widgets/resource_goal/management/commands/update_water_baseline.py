"""Invocation:  python manage.py update_water_baseline

update the daily baseline."""

import datetime
from apps.widgets.resource_goal import resource_goal
from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand


class Command(MakahikiBaseCommand):
    """command"""
    help = 'Update water baseline for all teams'

    def handle(self, *args, **options):
        """update the daily baseline"""
        today = datetime.datetime.today()
        print '****** Processing update_water_baseline for %s *******\n' % today

        today = today.date()
        # update the baseline
        resource_goal.update_resource_baseline("water", today, 2)
