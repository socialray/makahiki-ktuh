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
        make_option('--end_date', '-e', dest='end_date',
                    help='End date of the baseline data, in the format of YYYY-MM-DD'),
        make_option('--weeks', '-w', dest='weeks',
                    help='number of weeks of the previous baseline data.'),
        )

    help = 'Calculate the energy baseline data for all teams'

    def handle(self, *args, **options):
        """Calculate the energy baseline data for all teams"""
        if not options["end_date"]:
            print "Please specify the end_date of the baseline data."
            sys.exit(2)

        if not options["weeks"]:
            print "Please specify the number of weeks of previous baseline data."
            sys.exit(2)

        end_date = datetime.datetime.strptime(options["end_date"], "%Y-%m-%d").date()
        weeks = int(options["weeks"])

        resource_goal.update_energy_baseline(end_date, weeks, "Fixed")
