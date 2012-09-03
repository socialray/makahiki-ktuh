"""Invocation:  python manage.py check_energy_goal

Checks whether or not each team made their energy goal, and awards points to team members if it's
at the end of the day."""

import datetime

from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand
from apps.widgets.resource_goal import resource_goal


class Command(MakahikiBaseCommand):
    """command"""
    help = 'Check the energy goal for all teams, award points for meeting the goal'

    def handle(self, *args, **options):
        """check the energy goal for all teams"""
        today = datetime.datetime.today()

        print '****** Processing check_energy_goal for %s *******\n' % today

        # check the previous day's data and goal
        usage_date = today - datetime.timedelta(days=1)
        usage_date = datetime.datetime(usage_date.year, usage_date.month, usage_date.day,
                                       hour=23, minute=59, second=59)
        resource_goal.check_resource_goals("energy", usage_date)

        # update the baseline
        resource_goal.update_resource_baseline("energy", today.date(), 2)
