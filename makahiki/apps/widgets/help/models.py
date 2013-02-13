"""The model for help topics."""
from django.conf import settings
from django.db import models

HELP_CATEGORIES = (
    ("faq", "Frequently Asked Questions"),
    ("rules", "Rules of the competition"),
    ("widget", "Widget Help"),
    )
"""Defines the available help categories."""


class HelpTopic(models.Model):
    """Represents a help topic in the system."""

    title = models.CharField(max_length=255,
        help_text="The title of the topic.")
    slug = models.SlugField(help_text="Automatically generated if left blank.")
    category = models.CharField(max_length=50, choices=HELP_CATEGORIES,
                                help_text="One of the HELP_CATEGORIES.")
    priority = models.IntegerField(
        default=0,
        help_text="sorting order within the category. lower priority first "
    )
    contents = models.TextField(
        help_text="The content of the help topic. %s" % settings.MARKDOWN_TEXT)
    parent_topic = models.ForeignKey("HelpTopic",
        null=True,
        blank=True,
        help_text="Optional parent topic of this topic.",
        related_name="sub_topics",
    )
    admin_tool_tip = "The set of help topics in the challenge."

    @models.permalink
    def get_absolute_url(self):
        """Returns the absolute url for a help page."""
        return ('help_topic', [self.category, self.slug])

    def __unicode__(self):
        return "%s: %s" % (self.category.capitalize(), self.title)

    class Meta:
        """Meta"""
        ordering = ["category", "priority", ]
