"""Invocation: python manage.py reset_users <user email> [<user email>]*

Resets the user(s) as if they never took part in the competition. Preserves these attributes:
  * username
  * email
  * RA status
  * admin status
  * display_name
  * first and last name
  * team
"""

from django.core import management
from django.contrib.auth.models import User
from apps.managers.player_mgr import player_mgr


class Command(management.base.BaseCommand):
    """reset_users command"""

    help = 'Resets the user(s) as if they never took part in the competition.'

    def handle(self, *args, **options):
        """Resets the user as if they never took part in the competition."""
        if len(args) == 0:
            self.stdout.write("Need at least one username to reset.\n")
            return

        self.stdout.write(
            "WARNING: This command will reset the following user(s):\n%s" % (
                "\n".join(args)
                ))
        self.stdout.write("\n\nThis process is irreversible.\n")
        value = raw_input("Do you wish to continue (Y/n)? ")
        while value != "Y" and value != "n":
            self.stdout.write("Invalid option %s\n" % value)
            value = raw_input("Do you wish to continue (Y/n)? ")
        if value == "n":
            self.stdout.write("Operation cancelled.\n")
            return

        users = []
        for arg in args:
            try:
                users.append(User.objects.get(username=arg))
            except User.DoesNotExist:
                self.stdout.write(
                    "User '%s' does not exist. Aborting.\n" % (arg,))
                return

        for user in users:
            self.stdout.write("Resetting user %s\n" % user.username)
            player_mgr.reset_user(user)
