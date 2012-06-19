"""Invocation:  python manage.py clear_cache

Clear all content in the Makahiki cache."""

from apps.managers.cache_mgr import cache_mgr
from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand


class Command(MakahikiBaseCommand):
    """Management Command"""
    help = 'Clear all content in the makahiki cache.'

    def handle(self, *args, **options):
        """handle clear cache"""

        cache_mgr.clear()
        print "makahiki cache cleared."
