""" Utility command for creating or deleting test users.
Invocation: python manage.py test_users create <number_of_users>
or python manage.py test_users delete.
"""
import datetime

from django.contrib.auth.models import User
from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand
from apps.managers.team_mgr.models import Team


class Command(MakahikiBaseCommand):
    """create test users command"""

    help = 'create ot delete test users. \n'\
           'Usage: manage.py test_users create <number_of_users for each team>, or \n'\
           ' manage.py test_users delete'

    def handle(self, *args, **options):
        """create test users."""

        if len(args) == 0:
            self.stdout.write("Please specify create or delete.\n")
            return

        operation = args[0]
        if operation == 'create':

            if len(args) == 1:
                self.stdout.write("Please specify the number of test users for each team.\n")
                return

            count = int(args[1])
            self.create_test_users(count)

        elif operation == 'delete':
            self.delete_test_users()
        else:
            self.stdout.write("Invalid operation. please specify create or delete\n")

    def create_test_users(self, count):
        """Create the specified number of test users for each team."""
        total_count = 0
        for team in Team.objects.all():
            for i in range(0, count):
                username = "testuser-%s-%d" % (team.slug, i)
                user = User.objects.create_user(username,
                                                username + "@test.com",
                                                password="testuser")
                profile = user.get_profile()
                profile.setup_complete = True
                profile.setup_profile = True
                profile.team = team
                profile.save()
                profile.add_points(25, datetime.datetime.today(), 'test points for raffle')
                total_count += 1

        self.stdout.write("%d test users created.\n" % total_count)

    def delete_test_users(self):
        """delete the test users name start with 'testuser-'."""
        users = User.objects.filter(username__startswith="testuser-")
        total_count = 0
        for user in users:
            user.delete()
            total_count += 1
        self.stdout.write("%d test users deleted.\n" % total_count)
