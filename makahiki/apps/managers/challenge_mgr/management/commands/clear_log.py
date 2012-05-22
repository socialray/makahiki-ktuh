"""Command to clear all content in the makahiki log table."""
from apps.managers.log_mgr import log_mgr
from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand


class Command(MakahikiBaseCommand):
    """command"""
    help = 'clear all content in the makahiki cache.'

    def handle(self, *args, **options):
        """handle clear log"""

        log_mgr.clear()
        print "makahiki log cleared.\n"
