"""Prepare rendering of popular smart grid actions widget"""

from apps.widgets.smartgrid import   get_popular_tasks


def supply(request, page_name):
    """Supply view_objects content, which are the popular actions from the smart grid game."""

    _ = request
    _ = page_name
    return {
        "popular_tasks": get_popular_tasks(),
        }
