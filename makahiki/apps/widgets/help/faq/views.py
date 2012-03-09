"""Provides the view for the Help FAQ widget"""

from apps.widgets.help.models import HelpTopic


def supply(request, page_name):
    """ supply view_objects for widget rendering, namely the faq objects."""
    _ = request
    _ = page_name
    faqs = HelpTopic.objects.filter(category="faq", parent_topic__isnull=True)
    return {
        "faqs": faqs,
        }
