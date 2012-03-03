"""Prepare rendering of popular task widget"""
from apps.widgets.smartgrid import   get_popular_tasks


def supply(request, page_name):
    """supply view_objects content"""

    _ = request
    _ = page_name
    return {
        "popular_tasks": get_popular_tasks(),
        }
