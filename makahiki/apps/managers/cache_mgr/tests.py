"""Tests the cache_mgr module."""

from django.test import TransactionTestCase
import os
from apps.managers.cache_mgr import cache_mgr


class BaseUnitTestCase(TransactionTestCase):
    """basic setting test"""
    def testCache(self):
        """Tests basic cache operations."""
        self.assertTrue(cache_mgr.info() is not None,
                         "Test that info() return something.")
        self.assertEqual(len(cache_mgr.keys()), 0,
                         "Test that the current cache is empty.")

        cache_mgr.set_cache('test_key', 'test_value')
        self.assertEqual(len(cache_mgr.keys()), 1,
                         "Test that the current cache is not empty after set.")

        if 'MAKAHIKI_MEMCACHED_ENABLED' in os.environ and \
            os.environ['MAKAHIKI_MEMCACHED_ENABLED'] == "True":
            self.assertEqual(cache_mgr.get_cache('test_key'), 'test_value',
                             "Test get the correct value from cache.")

        cache_mgr.get_cache('test_key_2', 'default_value')
        self.assertEqual(len(cache_mgr.keys()), 2,
                             "Test that the current cache after get default.")

        cache_mgr.delete('test_key')
        self.assertEqual(len(cache_mgr.keys()), 1,
                         "Test delete from cache.")

        cache_mgr.clear()
        self.assertEqual(len(cache_mgr.keys()), 0,
                         "Test that the current cache is empty after clear.")
