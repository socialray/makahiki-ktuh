"""Invocation:  python manage.py load_users <file.csv> [RA]

Load and create the users from a csv file. The format of the csv file is:

team, firstname, lastname, email[, RA]

quoting around the column is supported.

"""
import csv
from django.core import management
from apps.managers.player_mgr import player_mgr


class Command(management.base.BaseCommand):
    """Load user command."""

    help = "manage.py load_users <file.csv> \n load and create the users from a csv file."

    lastname = None
    firstname = None
    username = None
    email = None
    team = None
    is_ra = False

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

        load_count = 0
        reader = csv.reader(infile)
        for row in reader:
            self.parse(row)
            player_mgr.create_player(self.username, self.email, self.firstname,
                                     self.lastname, self.team, self.is_ra)
            load_count += 1

        infile.close()
        print "---- total loaded: %d" % (load_count)

    def parse(self, items):
        """Parse the line."""

        self.team = items[0].strip().capitalize()

        self.firstname = items[1].strip().capitalize()
        self.lastname = items[2].strip().capitalize()

        self.email = items[3].strip()
        self.username = self.email.split("@")[0]

        if len(items) == 5:
            self.is_ra = True if items[4].strip().lower() == "ra" else False
        else:
            self.is_ra = False

        print "%s,%s,%s,%s,%s,%s" % (self.team, self.firstname, self.lastname, self.email,
          self.username, self.is_ra)
