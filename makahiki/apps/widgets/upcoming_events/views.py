"""Prepare the rendering for upcoming_events widget.

Depends on smartgrid widget.
"""

from apps.widgets.smartgrid.forms import EventCodeForm
from apps.widgets.smartgrid import get_available_events
from django.core.cache import cache


def supply(request, page_name):
    """supply the view_objects for this widget."""

    _ = page_name
    user = request.user
    events = cache.get('user_events-%s' % user.username)
    if not events:
        events = get_available_events(user)
        # Cache the user_event for a day
        cache.set('user_events-%s' % user.username,
            events, 60 * 60)

    event_form = EventCodeForm()

    return  {"events": events,
             "event_form": event_form}
