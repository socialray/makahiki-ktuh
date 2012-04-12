"""check energy goal command"""
import datetime

from django.core import management
from apps.managers.team_mgr.models import Team
from apps.widgets.energy_goal import energy_goal


class Command(management.base.BaseCommand):
    """command"""
    help = 'Check the energy goal for all teams, award points for meeting the goal'

    def handle(self, *args, **options):
        """check the energy goal for all teams"""
        print '****** Processing check_energy_goal for %s *******\n' % datetime.datetime.today()

        for team in Team.objects.all():
            count = energy_goal.check_daily_energy_goal(team)
            goal_points = team.energygoalsettings_set.all()[0].goal_points
            print '%s users in %s are awarded %s points each.' % (count,
                                                                  team,
                                                                  goal_points)
