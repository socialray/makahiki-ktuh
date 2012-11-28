"""Invocation:  python manage.py run_analysis

Run the data collection and analysis."""

import datetime
from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand
from apps.widgets.status import analysis


class Command(MakahikiBaseCommand):
    """command"""
    help = 'Run the data collection and analysis.'

    def handle(self, *args, **options):
        """Run the data collection and analysis."""
        today = datetime.datetime.today()
        print '****** Processing data analysis at %s.*******\n' % today

        #print analysis.calculate_summary_stats()
        #print analysis.calculate_action_stats()
        #print analysis.calculate_user_stats()

        outfile = open('user_timestamps.csv', 'w')
        analysis.user_timestamps(None, "2012-09-04", "2012-10-01", outfile)
        outfile.close()

        outfile = open('user_point_timestamps.csv', 'w')
        analysis.user_point_timestamps("2012-09-04", "2012-10-01", outfile)
        outfile.close()

        outfile = open('energy_goal_timestamps.csv', 'w')
        analysis.energy_goal_timestamps("2012-09-04", "2012-10-01", outfile)
        outfile.close()

        today = datetime.datetime.today()
        print '****** End processing data analysis at %s.*******\n' % today
