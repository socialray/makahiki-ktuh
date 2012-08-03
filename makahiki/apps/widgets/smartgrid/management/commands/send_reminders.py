"""Invocation:  python manage.py send_reminders
send out reminders. Normally is scheduled hourly.
"""

import datetime

from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand
from apps.widgets.smartgrid import smartgrid


class Command(MakahikiBaseCommand):
    """command"""
    help = 'Send out reminders'

    def handle(self, *args, **options):
        """send reminders"""
        print '****** Processing send_reminders at %s *******\n' % datetime.datetime.today()
        smartgrid.send_reminders()
