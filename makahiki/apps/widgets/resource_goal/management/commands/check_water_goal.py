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
        today = datetime.datetime.today()

        print '****** Processing check_water_goal for %s *******\n' % today

        # check the previous day's data and goal
        resource_goal.check_resource_goals("water", today - datetime.timedelta(days=1))

        # update the baseline for today
        resource_goal.update_resource_baseline("water", today.date(), 2)
