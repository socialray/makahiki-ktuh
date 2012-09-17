"""Invocation:  python manage.py process_rounds
send out notifications as round transition, carry over the round scoreboard entries.
"""

import datetime

from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand
from apps.widgets.smartgrid import smartgrid


class Command(MakahikiBaseCommand):
    """command"""
    help = 'Send out notifications as round transition, carry over round scoreboard.'

    def handle(self, *args, **options):
        """process daily notices"""
        print '****** Processing rounds at %s *******' % datetime.datetime.today()
        smartgrid.notify_round_started()
