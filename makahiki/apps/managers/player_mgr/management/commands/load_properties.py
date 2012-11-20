"""Invocation:  python manage.py load_properties <file.csv>

Load the profile properties from a csv file. The format of the csv file is:

username, properties_string

"""
from django.core import management
from apps.managers.player_mgr import player_mgr


class Command(management.base.BaseCommand):
    """Load user command."""

    help = "manage.py load_properties <file.csv> \n load the profile properties from a csv file."

    def handle(self, *args, **options):
        """Load the profile properties from a csv file"""
        if len(args) == 0:
            self.stdout.write("the properties csv file name missing.\n")
            return

        f = args[0]
        try:
            infile = open(f)
        except IOError:
            self.stdout.write(
                "Can not open the file: %s , Aborting.\n" % f)
            return

        load_count = player_mgr.bulk_load_player_properties(infile)

        infile.close()
        print "---- total loaded: %d" % load_count
