"""Prepare the rendering for upcoming_events widget.
   Depends on the smart grid game widget."""
from apps.managers.cache_mgr import cache_mgr
from apps.widgets.smartgrid.forms import EventCodeForm
from apps.widgets.smartgrid import smartgrid


def supply(request, page_name):
    """Supply the view_objects for this widget, which are the upcoming events."""

    _ = page_name
    user = request.user
    events = cache_mgr.get_cache('user_events-%s' % user.username)
    if not events:
        events = smartgrid.get_available_events(user)
        # Cache the user_event for a day
        cache_mgr.set_cache('user_events-%s' % user.username,
            events, 60 * 60)

    event_form = EventCodeForm()

    return  {"events": events,
             "event_form": event_form}
