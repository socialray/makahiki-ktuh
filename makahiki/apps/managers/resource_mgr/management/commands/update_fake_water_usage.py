"""Invocation:  python manage.py update_fake_water_usage

For each team, update the water usage with fake data. Because water usage input is manual,
this script should only be called once a day in the time specified in the manual_entry_time
of the ResourceGoalSetting."""

import datetime

from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand
from apps.managers.resource_mgr.models import WaterUsage
from apps.managers.team_mgr.models import Team


class Command(MakahikiBaseCommand):
    """command"""
    help = 'Update the fake water usage for all teams.'

    def handle(self, *args, **options):
        """Update the fake water usage for all teams"""
        date = datetime.datetime.today()
        print '****** Processing fake water usage update at %s *******\n' % date

        today = datetime.datetime.today()
        for team in Team.objects.all():
            count = team.profile_set.count()
            if count:
                # assume the average water usage is 80 gallon per person per day
                average_usage = 80
                actual_usage = average_usage * 0.9
                water, _ = WaterUsage.objects.get_or_create(team=team, date=today.date())
                water.time = today.time()
                water.usage = actual_usage * count
                water.save()
