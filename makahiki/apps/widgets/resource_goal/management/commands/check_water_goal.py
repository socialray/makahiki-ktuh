"""Invocation:  python manage.py check_water_goal

Checks whether or not each team made their water goal, and awards points to team members if it's
at the end of the day."""

import datetime

from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand
from apps.widgets.resource_goal import resource_goal


class Command(MakahikiBaseCommand):
    """command"""
    help = 'Check the water goal for all teams, award points for meeting the goal'

    def handle(self, *args, **options):
        """check the energy goal for all teams"""
        print '****** Processing check_water_goal for %s *******\n' % datetime.datetime.today()

        resource_goal.check_all_daily_resource_goals("water")
