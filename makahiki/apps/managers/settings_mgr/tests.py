"""Tests the settings_mgr module."""

import datetime
from django.contrib.auth.models import User

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings

from apps.managers.settings_mgr import  get_current_round
from apps.template_support.templatetags.class_tags import insert_classes, get_id_and_classes
from apps.css_rules import default
from apps.test_helpers.test_utils import TestUtils


class ContextProcessorFunctionalTestCase(TestCase):
    """Tests that the proper variables are loaded into a page."""

    def testRoundInfo(self):
        """Tests that round info is available for the page to process."""
        TestUtils.set_competition_round()
        current_round = get_current_round()

        User.objects.create_user("user", "user@test.com", password="changeme")
        self.client.login(username="user", password="changeme")

        response = self.client.get(reverse("home_index"))
        # Response context should have round info corresponding to the past days.

        self.assertEqual(response.context["CURRENT_ROUND_INFO"]["name"], current_round,
            "Expected %s but got %s" % (
                current_round, response.context["CURRENT_ROUND_INFO"]["name"]))


class BaseUnitTestCase(TestCase):
    """basic setting test"""
    def testCurrentRound(self):
        """Tests that the current round retrieval is correct."""
        current_round = "Round 1"

        TestUtils.set_competition_round()

        current = get_current_round()
        self.assertEqual(current, current_round,
            "Test that the current round is returned.")

        start = datetime.datetime.today() + datetime.timedelta(days=1)
        end = start + datetime.timedelta(days=7)
        settings.COMPETITION_ROUNDS = {
            "Round 1": {"start": start, "end": end, }, }

        current_round = get_current_round()
        self.assertTrue(current_round is None,
            "Test that there is no current round.")


class ClassTagsUnitTests(TestCase):
    """ test class tags
    """
    def setUp(self):
        """Stores the current values of the CSS keys so that we can modify
        them."""
        self.saved_classes = default.CSS_CLASSES
        self.saved_ids = default.CSS_IDS
        default.CSS_CLASSES = {"foo": "bar"}
        default.CSS_IDS = {"foo_id": "bar_id"}

    def testEmptyClassRetrieval(self):
        """Checks that disabling RETURN_CLASSES returns empty strings for
        classes."""
        saved_setting = default.RETURN_CLASSES
        default.RETURN_CLASSES = False
        class_name = default.CSS_CLASSES.keys()[0]
        self.assertEqual(insert_classes(class_name), "",
            "Check that insert classes now returns an empty string.")

        # Restore setting
        default.RETURN_CLASSES = saved_setting

    def testDisabledIdExpansion(self):
        """Tests the ability to expand an id into an id and classes."""
        saved_setting = default.RETURN_CLASSES
        default.RETURN_CLASSES = False

        tag_id = default.CSS_IDS.keys()[0]
        expected_string = 'id="%s"' % (tag_id,)
        self.assertEqual(get_id_and_classes(tag_id), expected_string,
            "Expected: %s but got %s." % (
                expected_string, get_id_and_classes(tag_id)))

        # Restore setting
        default.RETURN_CLASSES = saved_setting

    def tearDown(self):
        default.CSS_CLASSES = self.saved_classes
        default.CSS_IDS = self.saved_ids
