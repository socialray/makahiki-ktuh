"""Invocation:  python manage.py cal_energy_baseline

Calculate the energy baseline data for all teams, from the history energy data."""

import datetime
import requests

from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand
from apps.managers.resource_mgr import resource_mgr
from apps.managers.team_mgr.models import Team
from apps.widgets.resource_goal.models import EnergyBaselineDaily, EnergyBaselineHourly


BASELINE_PERIOD_WEEKS = 2
"""number of weeks of the history data used for baseline calculation."""


class Command(MakahikiBaseCommand):
    """command"""
    help = 'Calculate the energy baseline data for all teams'

    def handle(self, *args, **options):
        """Calculate the energy baseline data for all teams"""
        session = requests.session()

        # energy daily
        for baseline in EnergyBaselineDaily.objects.all():
            baseline.delete()

        start_date = datetime.date.today() - datetime.timedelta(weeks=BASELINE_PERIOD_WEEKS)
        for team in Team.objects.all():
            for day in range(0, 7):
                usage = resource_mgr.get_daily_energy_baseline_usage(
                    session, team, day, start_date, BASELINE_PERIOD_WEEKS)
                EnergyBaselineDaily(team=team, day=day, usage=usage).save()
            print 'team %s energy baseline daily usage updated.' % team

        # energy hourly
        for baseline in EnergyBaselineHourly.objects.all():
            baseline.delete()
        for team in Team.objects.all():
            for day in range(0, 7):
                for hour in range(1, 25):
                    usage = resource_mgr.get_hourly_energy_baseline_usage(
                        session, team, day, hour, start_date, BASELINE_PERIOD_WEEKS)
                    EnergyBaselineHourly(team=team, day=day, hour=hour, usage=usage).save()
            print 'team %s energy baseline hourly usage updated.' % team
