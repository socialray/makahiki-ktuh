"""Invocation:  python manage.py load_users <file.csv> [RA]

Load and create the users from a csv file containing lounge, name, and email.
If the second argument is RA, then the csv file is the RA list, consists of name,
email, lounge.

.. note:: This command has UH-specific code in it and must be revised.
"""
from django.core import management
from apps.managers.player_mgr import player_mgr


class Command(management.base.BaseCommand):
    """Load user command."""

    help = """load and create the users from a csv file containing lounge,
     name, and email, if the second argument is RA, the csv file is the RA
     list, consists of name, email, lounge."""

    lastname = None
    firstname = None
    username = None
    email = None
    lounge = None
    is_ra = False

    def handle(self, *args, **options):
        """Load and create the users from a csv file containing lounge, name, and email."""
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

        error_count = 0
        load_count = 0
        for line in infile:
            if not self.parse_ok(line):
                error_count += 1
            else:
                player_mgr.create_player(self.username, self.email, self.firstname,
                                         self.lastname, self.lounge)
                load_count += 1

        infile.close()
        print "---- total loaded: %d , errors: %d" % (load_count, error_count)

    def parse_ok(self, line):
        """Parse the line.
           :return false if there is an error."""

        items = line.split(":")

        if self.is_ra:
            names = items[0].split(",")
            self.lastname = names[0].strip().capitalize()
            self.firstname = names[1].strip().capitalize()
            self.username = items[1].strip()
            self.email = self.username + "@hawaii.edu"

            lounge_items = items[2].split()
            self.lounge = get_lounge(lounge_items[0].strip(),
                lounge_items[1].strip().zfill(4)[:2])
        else:
            lounge_items = items[0].split()

            self.lounge = get_lounge(lounge_items[2], lounge_items[3])

            self.firstname = items[1].strip().capitalize()
            middlename = items[2].strip().capitalize()
            if middlename:
                self.firstname += " " + middlename

            self.lastname = items[3].strip().capitalize()
            self.email = items[4].strip()
            self.username = self.email.split("@")[0]

        print "%s,%s,%s,%s,%s" % (
            self.lounge, self.firstname, self.lastname, self.email,
            self.username)

        if not self.email.endswith("@hawaii.edu"):
            print "==== ERROR ==== non-hawaii edu email: %s" % (self.email)
            return False
        else:
            return True

        def get_lounge(dorm, team):
            """returns the lounge name"""
            return get_dorm(dorm) + '-' + get_team(team)

        def get_dorm(dorm):
            """Returns the dorm name."""
            return {
                'LE': 'Lehua',
                'MO': 'Mokihana',
                'IL': 'Ilima',
                'LO': 'Lokelani'}[dorm]

        def get_team(team):
            """ Returns the team name."""
            return {
                '03': 'A',
                '04': 'A',
                '05': 'B',
                '06': 'B',
                '07': 'C',
                '08': 'C',
                '09': 'D',
                '10': 'D',
                '11': 'E',
                '12': 'E'}[team]
