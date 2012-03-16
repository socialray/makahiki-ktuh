"""check energy goal command"""
import datetime

from django.core import management
from apps.widgets.energy_goal.models import TeamEnergyGoal


class Command(management.base.BaseCommand):
    """command"""
    help = 'Check the energy goal for all teams, award points for meeting the goal'

    def handle(self, *args, **options):
        """check the energy goal for all teams"""
        print '****** Processing check_energy_goal for %s *******\n' % datetime.datetime.today()

        for goal in TeamEnergyGoal.objects.all():
            goal.award_goal_points()
