"""Invocation:  python manage.py load_users <file.csv> [RA]

Load and create the users from a csv file. The format of the csv file is:

team, firstname, lastname, email, username, password[, RA]

quoting around the column is supported.

"""
from django.core import management
from apps.managers.player_mgr import player_mgr


class Command(management.base.BaseCommand):
    """Load user command."""

    help = "manage.py load_users <file.csv> \n load and create the users from a csv file."

    def handle(self, *args, **options):
        """Load and create the users from a csv file containing team, name, and email."""
        if len(args) == 0:
            self.stdout.write("the csv file name missing.\n")
            return

        filename = args[0]
        try:
            infile = open(filename)
        except IOError:
            self.stdout.write(
                "Can not open the file: %s , Aborting.\n" % (filename))
            return

        load_count = player_mgr.bulk_create_players(infile)

        infile.close()
        print "---- total loaded: %d" % (load_count)
