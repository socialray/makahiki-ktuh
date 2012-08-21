"""Invocation:  python manage.py cal_energy_baseline

Calculate the energy baseline data for all teams, from the history energy data."""

import datetime
from optparse import make_option
import sys

from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand
from apps.widgets.resource_goal import resource_goal


class Command(MakahikiBaseCommand):
    """command"""
    option_list = MakahikiBaseCommand.option_list + (
        make_option('--start_date', '-s', dest='start_date',
                    help='Start date of the baseline data, in the format of YYYY-MM-DD'),
        make_option('--weeks', '-w', dest='weeks',
                    help='number of weeks of the baseline data'),
        )

    help = 'Calculate the energy baseline data for all teams'

    def handle(self, *args, **options):
        """Calculate the energy baseline data for all teams"""
        if not options["start_date"]:
            print "Please specify the start_date of the baseline data."
            sys.exit(2)

        if not options["weeks"]:
            print "Please specify the number of weeks of baseline data."
            sys.exit(2)

        start_date = datetime.datetime.strptime(options["start_date"], "%Y-%m-%d").date()
        weeks = int(options["weeks"])

        resource_goal.cal_energy_baseline(start_date, weeks)
