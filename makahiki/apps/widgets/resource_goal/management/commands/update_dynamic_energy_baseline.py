"""Invocation:  python manage.py update_dynamic_energy_baseline

Calculate the dynamic energy baseline data for all teams, from the history energy data."""

import datetime
from optparse import make_option
import sys

from apps.widgets.resource_goal import resource_goal
from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand


class Command(MakahikiBaseCommand):
    """command"""
    option_list = MakahikiBaseCommand.option_list + (
        make_option('--weeks', '-w', dest='weeks',
                    help='number of weeks of the baseline data'),
        )

    help = 'update the dynammic energy baseline data for all teams'

    def handle(self, *args, **options):
        """Calculate the energy baseline data for all teams"""
        if not options["weeks"]:
            print "Please specify the number of weeks of baseline data."
            sys.exit(2)

        weeks = int(options["weeks"])

        today = datetime.datetime.today()
        print '****** Processing update_dynamic_energy_baseline for %s *******\n' % today

        resource_goal.update_energy_baseline(today.date(), weeks, "Dynamic")
