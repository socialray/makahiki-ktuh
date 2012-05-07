"""Implements the view for the widget providing an introduction to the challenge."""
from apps.widgets.smartgrid import smartgrid


def supply(request, page_name):
    """ supply view_objects for widget rendering."""
    _ = request
    _ = page_name
    video_action = smartgrid.get_setup_activity()
    return {"video_action": video_action}
