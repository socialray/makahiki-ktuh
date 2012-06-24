"""Prepare the rendering for upcoming_events widget.
   Depends on the smart grid game widget."""
from apps.widgets.smartgrid.forms import EventCodeForm
from apps.widgets.smartgrid import smartgrid


def supply(request, page_name):
    """Supply the view_objects for this widget, which are the upcoming events."""

    _ = page_name
    user = request.user
    events = smartgrid.get_available_events(user)
    event_form = EventCodeForm()

    return  {"events": events,
             "event_form": event_form}
