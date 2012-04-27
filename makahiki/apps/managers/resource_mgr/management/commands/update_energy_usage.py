"""check energy goal command"""
import datetime

from django.core import management
from apps.managers.resource_mgr import resource_mgr
from apps.managers.team_mgr.models import Team


class Command(management.base.BaseCommand):
    """command"""
    help = 'Update the energy usage for all teams from wattdepot server.'

    def handle(self, *args, **options):
        """check the energy goal for all teams"""
        date = datetime.datetime.today()
        print '****** Processing energy usage updater at %s *******\n' % date

        for team in Team.objects.all():
            resource_mgr.update_energy_usage(date, team)
            print 'team %s energy usage updated.' % team
