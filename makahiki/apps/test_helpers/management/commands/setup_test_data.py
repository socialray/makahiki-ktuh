"""setup test data command"""
import datetime

from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand
from apps.managers.challenge_mgr.models import RoundSettings
from apps.managers.team_mgr.models import Team
from apps.widgets.resource_goal.models import EnergyGoalSetting, EnergyBaselineHourly, \
    EnergyBaselineDaily, WaterGoalSetting
from apps.widgets.smartgrid.models import Event


class Command(MakahikiBaseCommand):
    """command"""
    help = 'Setup the test data, including: \n ' \
           'round dates, resource baselines, event dates'

    def handle(self, *args, **options):
        """set up the test data"""
        self.setup_rounds()
        self.setup_event_dates()
        self.setup_resource_baseline()
        self.setup_resource_goalsetting()

    def setup_rounds(self):
        """set up test rounds, any existing rounds will be deleted."""

        for r in RoundSettings.objects.all():
            r.delete()

        start = datetime.datetime.today()
        end1 = start + datetime.timedelta(days=7)
        end2 = end1 + datetime.timedelta(days=7)
        overall_end = end2 + datetime.timedelta(days=7)

        RoundSettings(name="Round 1", start=start, end=end1).save()
        RoundSettings(name="Round 2", start=end1, end=end2).save()
        RoundSettings(name="Overall", start=end2, end=overall_end).save()

    def setup_event_dates(self):
        """set up event dates."""
        for event in Event.objects.all():
            event_day_delta = event.event_date.date() - datetime.date(2011, 10, 17)
            event.event_date = datetime.datetime.today() + event_day_delta

            pub_day_delta = event.pub_date - datetime.date(2011, 10, 17)
            event.pub_date = datetime.date.today() + pub_day_delta

            event.save()

    def setup_resource_baseline(self):
        """set up the resource baseline data, all existing data will be delete."""

        for baseline in EnergyBaselineHourly.objects.all():
            baseline.delete()

        for team in Team.objects.all():
            for day in range(0, 7):
                for hour in range(1, 25):
                    EnergyBaselineHourly(team=team, day=day, hour=hour, usage=1000 * hour).save()

        for baseline in EnergyBaselineDaily.objects.all():
            baseline.delete()

        for team in Team.objects.all():
            for day in range(0, 7):
                EnergyBaselineDaily(team=team, day=day, usage=1000 * 24).save()

    def setup_resource_goalsetting(self):
        """set up the resource goal data. all existing data will be delete."""
        for goal_setting in EnergyGoalSetting.objects.all():
            goal_setting.delete()

        for team in Team.objects.all():
            EnergyGoalSetting(team=team,
                              goal_percent_reduction=5,
                              warning_percent_reduction=3,
                              manual_entry=False,
                              manual_entry_time=datetime.time(15),
                              goal_points=20).save()

        for goal_setting in WaterGoalSetting.objects.all():
            goal_setting.delete()

        for team in Team.objects.all():
            WaterGoalSetting(team=team,
                              goal_percent_reduction=5,
                              warning_percent_reduction=3,
                              manual_entry=True,
                              manual_entry_time=datetime.time(15),
                              goal_points=20).save()
