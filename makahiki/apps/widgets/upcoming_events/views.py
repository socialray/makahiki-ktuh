from django.core.cache import cache

from widgets.smartgrid.models import *
from widgets.smartgrid.forms import *

def supply(request):
    user = request.user
    events = cache.get('user_events-%s' % user.username)
    if not events:
        events = get_available_events(user)
        # Cache the user_event for a day
        cache.set('user_events-%s' % user.username,
            events, 60 * 60)

    event_form = EventCodeForm()

    return  { "events" : events,
              "event_form" : event_form }