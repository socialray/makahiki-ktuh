"""Invocation:  python manage.py check_energy_goal

Checks whether or not each team made their energy goal, and awards points to team members if it's
at the end of the day."""

import datetime

from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand
from apps.managers.resource_mgr import resource_mgr
from apps.widgets.resource_goal import resource_goal


class Command(MakahikiBaseCommand):
    """command"""
    help = 'Check the energy goal for all teams, award points for meeting the goal'

    def handle(self, *args, **options):
        """check the energy goal for all teams"""
        today = datetime.datetime.today()

        print '****** Processing check_energy_goal for %s *******\n' % today

        # update the latest resource usage before checking
        resource_mgr.update_energy_usage()

        # update the dynamic baseline if they are dynamic
        resource_goal.update_energy_baseline(today.date(), 2, "Dynamic")

        resource_goal.check_all_daily_resource_goals("energy")
