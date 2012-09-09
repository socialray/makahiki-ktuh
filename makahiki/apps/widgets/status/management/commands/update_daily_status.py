"""Invocation:  python manage.py update_daily_status

Update the number of users that logged in today.
"""

import datetime
from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand
from apps.widgets.status import status


class Command(MakahikiBaseCommand):
    """command"""
    help = 'Update the number of daily users.'

    def handle(self, *args, **options):
        """Update the number of users that logged in today."""
        today = datetime.datetime.today()
        print '****** Processing daily user count update at %s.*******\n' % today

        status.update_daily_status()
