"""Invocation:  python manage.py process_notices
send out notifications such as round transition, commitment end, and process rsvps.
should be scheduled daily at the beginning of the day.
"""

import datetime

from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand
from apps.widgets.badges import badges
from apps.widgets.smartgrid import smartgrid


class Command(MakahikiBaseCommand):
    """command"""
    help = 'Send out notifications such as round transition, commitment end, and process rsvps.'

    def handle(self, *args, **options):
        """process daily notices"""
        print '****** Processing notices at %s *******' % datetime.datetime.today()
        smartgrid.notify_commitment_end()
        smartgrid.process_rsvp()
        smartgrid.check_daily_submissions()
        badges.award_possible_daily_badges()
