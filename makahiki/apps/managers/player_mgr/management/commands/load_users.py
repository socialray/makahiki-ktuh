"""Invocation:  python manage.py load_users <file.csv> [RA]

Load and create the users from a csv file. The format of the csv file is:

"team","firstname,middlename,lastname","email"

If the second argument is RA, then the csv file is the RA list.

"""
import csv
from django.core import management
from apps.managers.player_mgr import player_mgr


class Command(management.base.BaseCommand):
    """Load user command."""

    help = """manage.py load_users <file.csv> [RA] \n
     load and create the users from a csv file containing team,
     name, and email, if the second argument is RA, the csv file is the RA
     list."""

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

        if len(args) > 1:
            if args[1] == 'RA':
                self.is_ra = True
            else:
                self.stdout.write("the second argument can only be RA.\n")
                return

        load_count = 0

        reader = csv.reader(infile)
        for row in reader:
            self.parse(row)
            player_mgr.create_player(self.username, self.email, self.firstname,
                                     self.lastname, self.team)
            load_count += 1

        infile.close()
        print "---- total loaded: %d" % (load_count)

    def parse(self, items):
        """Parse the line."""

        self.team = items[0]

        fullname = items[1].split(',')
        self.firstname = fullname[0].strip().capitalize()
        middlename = fullname[1].strip().capitalize()
        if middlename:
            self.firstname += " " + middlename
        self.lastname = fullname[2].strip().capitalize()

        self.email = items[2].strip()
        self.username = self.email.split("@")[0]

        print "%s,%s,%s,%s,%s" % (self.team, self.firstname, self.lastname, self.email,
          self.username)
