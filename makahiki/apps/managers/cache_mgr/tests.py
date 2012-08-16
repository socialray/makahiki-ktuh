"""Tests the cache_mgr module."""

from django.test import TransactionTestCase
from apps.managers.cache_mgr import cache_mgr
from django.conf import settings


class BaseUnitTestCase(TransactionTestCase):
    """basic setting test"""
    def testCache(self):
        """Tests basic cache operations."""
        self.assertTrue(cache_mgr.info() is not None,
                         "Test that info() return something.")
        cache_mgr.set_cache('test_key', 'test_value')

        if settings.MAKAHIKI_USE_MEMCACHED:
            self.assertEqual(cache_mgr.get_cache('test_key'), 'test_value',
                             "Test get the correct value from cache.")

        cache_mgr.delete('test_key')
        self.assertEqual(cache_mgr.get_cache('test_key'), None,
                         "Test get the correct value from cache.")

        cache_mgr.clear()
        self.assertEqual(cache_mgr.get_cache('test_key'), None,
                         "Test get the correct value from cache.")
