"""Invocation:  python manage.py award_participation

Checks whether or not each team's participation rate, and awards points to team members if meets
certain criteria."""

import datetime

from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand
from apps.widgets.participation import participation


class Command(MakahikiBaseCommand):
    """command"""
    help = 'Award points for meeting the active participation rate.'

    def handle(self, *args, **options):
        """check the energy goal for all teams"""
        print '****** Processing award participation for %s *******\n' % datetime.datetime.today()

        participation.award_participation()
