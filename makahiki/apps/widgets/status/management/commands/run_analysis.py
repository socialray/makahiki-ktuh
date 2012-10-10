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

        print analysis.calculate_summary_stats()
        print analysis.calculate_action_stats()
        analysis.calculate_user_stats()
