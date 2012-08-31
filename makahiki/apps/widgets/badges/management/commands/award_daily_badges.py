"""Invocation:  python manage.py award_daily_badges

scheduled to be run at the beginning of the day. it checks all the active users and award
possible daily badges to them."""

import datetime

from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand
from apps.widgets.badges import badges


class Command(MakahikiBaseCommand):
    """command"""
    help = 'Award the daily badges to all active users.'

    def handle(self, *args, **options):
        """Update the energy usage for all teams."""
        date = datetime.datetime.today()
        print '****** Processing award daily badges at %s *******\n' % date
        badges.award_possible_daily_badges()
