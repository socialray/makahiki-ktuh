"""Invocation:  python manage.py clear_log

Clear all content in the Makahiki log table."""

from apps.managers.log_mgr import log_mgr
from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand


class Command(MakahikiBaseCommand):
    """command"""
    help = 'Clear all content in the makahiki log.'

    def handle(self, *args, **options):
        """handle clear log"""

        log_mgr.clear()
        print "makahiki log cleared.\n"
