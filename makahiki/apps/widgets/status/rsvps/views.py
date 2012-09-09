"""handles request for RSVP status."""

from django.db.models import Count
from apps.widgets.smartgrid.models import Action


def supply(request, page_name):
    """supply view_objects for RSVP status."""

    _ = page_name
    _ = request

    events = Action.objects.filter(
        type="event",
        actionmember__approval_status="pending",
    ).annotate(rsvps=Count('actionmember')).order_by('-rsvps').select_related('event')
    excursions = Action.objects.filter(
        type="excursion",
        actionmember__approval_status="pending",
    ).annotate(rsvps=Count('actionmember')).order_by('-rsvps').select_related('event')

    return {
        "events": events,
        "excursions": excursions,
        }
