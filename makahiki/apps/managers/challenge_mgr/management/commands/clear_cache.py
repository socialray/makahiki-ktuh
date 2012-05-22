"""Clear all content in the makahiki cache command"""
from apps.managers.cache_mgr import cache_mgr
from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand


class Command(MakahikiBaseCommand):
    """command"""
    help = 'clear all content in the makahiki cache.'

    def handle(self, *args, **options):
        """handle clear cache"""

        cache_mgr.clear()
        print "makahiki cache cleared.\n"
