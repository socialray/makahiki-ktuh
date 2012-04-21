"""Prepare rendering of popular smart grid actions widget"""

from apps.widgets.smartgrid import   smartgrid


def supply(request, page_name):
    """Supply view_objects content, which are the popular actions from the smart grid game."""

    _ = request
    _ = page_name
    return {
        "popular_tasks": smartgrid.get_popular_tasks(),
        }
