"""
views for Help Rule widget
"""

from managers.help_mgr.models import HelpTopic

def supply(request, page_name):
    """ supply view_objects for widget rendering."""
    _ = request
    _ = page_name
    rules = HelpTopic.objects.filter(category="rules", parent_topic__isnull=True)
    return {
        "rules": rules,
        }

