"""Tests the template tags."""

from django.test import TransactionTestCase
from apps.template_support.templatetags.class_tags import insert_classes, get_id_and_classes
from apps.css_rules import default


class ClassTagsUnitTests(TransactionTestCase):
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
