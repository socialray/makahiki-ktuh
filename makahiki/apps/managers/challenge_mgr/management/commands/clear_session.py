"""delete all persistent web sessions.
Use this to clean up any invalid session references."""

from django.core import management
from django.contrib.sessions.models import Session


class Command(management.base.BaseCommand):
    """command"""
    help = 'delete all persistent web sessions. ' \
           'Use this to clean up any invalid session references.'

    def handle(self, *args, **options):
        """delete all persistent web sessions"""

        Session.objects.all().delete()
        print "makahiki session cleared.\n"
