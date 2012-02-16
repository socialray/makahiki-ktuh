"""
views for Help FAQ widget
"""

from managers.help_mgr.models import HelpTopic

def supply(request):
    """ supply view_objects for widget rendering."""
    _ = request
    faqs = HelpTopic.objects.filter(category="faq", parent_topic__isnull=True)
    return {
        "faqs": faqs,
        }

