"""
test settings
"""

import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
from apps import test_utils

from apps.managers.settings_mgr import  get_current_round
from apps.templatetags.class_tags import insert_classes, get_id_and_classes
from apps.css_rules import default


class ContextProcessorFunctionalTestCase(TestCase):
    """Tests that the proper variables are loaded into a page."""


def setUp(self):
    """Sets up round and competition info to be at the start of round 2."""
    self.saved_rounds = settings.COMPETITION_ROUNDS
    self.saved_start = settings.COMPETITION_START
    self.saved_end = settings.COMPETITION_END

    self.current_round = "Round 2"

    start = datetime.datetime.today() - datetime.timedelta(days=7)
    end1 = start + datetime.timedelta(days=6)
    start2 = datetime.datetime.today()
    end2 = start2 + datetime.timedelta(days=6)

    settings.COMPETITION_ROUNDS = {
        "Round 1": {
            "start": start,
            "end": end1,
            },
        "Round 2": {
            "start": start2,
            "end": end2,
            },
        }

    settings.COMPETITION_START = start
    settings.COMPETITION_END = (end2 + datetime.timedelta(days=7)).strftime(
        "%Y-%m-%d %H:%M:%S")


def testRoundInfo(self):
    """Tests that round info is available for the page to process."""
    self.client.login(username="user", password="changeme")

    response = self.client.get(reverse("home_index"))
    # Response context should have round info corresponding to the past days.
    expected_info = {
        "Round 1": {
            "start": 7,
            "end": 2,
            },
        "Round 2": {
            "start": 0,
            "end": -5,
            },
        "Overall": {
            "start": 7,
            "end": -12,
            },
        }

    self.assertEqual(response.context["ROUNDS"], expected_info,
        "Expected %s but got %s" % (expected_info, response.context["ROUNDS"]))
    self.assertEqual(response.context["CURRENT_ROUND_INFO"]["name"], self.current_round,
        "Expected %s but got %s" % (
            self.current_round, response.context["CURRENT_ROUND_INFO"]["name"]))


def tearDown(self):
    """Restores saved rounds and competition info."""
    settings.COMPETITION_ROUNDS = self.saved_rounds
    settings.COMPETITION_START = self.saved_start
    settings.COMPETITION_END = self.saved_end


class BaseUnitTestCase(TestCase):
    """basic setting test"""
    def testCurrentRound(self):
        """Tests that the current round retrieval is correct."""
        saved_rounds = settings.COMPETITION_ROUNDS
        current_round = "Round 1"

        test_utils.set_competition_round()

        current = get_current_round()
        self.assertEqual(current, current_round,
            "Test that the current round is returned.")

        test_utils.set_competition_round()

        current_round = get_current_round()
        self.assertTrue(current_round is None,
            "Test that there is no current round.")

        # Restore settings.
        settings.COMPETITION_ROUNDS = saved_rounds


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

    def testDefaultClassRetrieval(self):
        """Checks that default values can be retrieved."""
        class_name = default.CSS_CLASSES.keys()[0]
        self.assertEqual(insert_classes(class_name),
            default.CSS_CLASSES[class_name],
            "Check that insert classes returns the correct value from the "
            "dictionary.")

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

    def testIdAndClassExpansion(self):
        """Tests the ability to expand an id into an id and classes."""
        tag_id = default.CSS_IDS.keys()[0]
        expected_string = 'id="%s" class="%s"' % (
            tag_id, default.CSS_IDS[tag_id])
        self.assertEqual(get_id_and_classes(tag_id), expected_string,
            "Expected: %s but got %s." % (
                expected_string, get_id_and_classes(tag_id)))

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
