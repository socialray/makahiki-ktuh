"""Invocation:  python manage.py send_reminders
send out reminders. Normally is scheduled hourly.
"""

import datetime

from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand
from apps.widgets.participation import participation
from apps.widgets.smartgrid import smartgrid


class Command(MakahikiBaseCommand):
    """command"""
    help = 'Send out reminders'

    def handle(self, *args, **options):
        """send reminders"""
        print '****** Processing send_reminders at %s *******' % datetime.datetime.today()
        smartgrid.send_reminders()
        smartgrid.check_new_submissions()
        participation.award_participation()
