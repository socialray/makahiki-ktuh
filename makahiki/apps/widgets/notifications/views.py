"""Handle the requests for the notification widget."""

from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect

from apps.widgets.notifications.models import UserNotification
from apps.widgets.notifications import get_unread_notifications


def supply(request, page_name):
    """Supply the view_objects content, which are the last 3 unread notifications."""
    _ = page_name
    return get_unread_notifications(request.user, limit=3)


def read(request, notification_id):
    """Handle the read notification request."""
    if not request.method == "POST":
        raise Http404

    if notification_id != "0":
        notification = get_object_or_404(UserNotification, pk=notification_id)
        notification.unread = False
        notification.save()
    else:
        for notification in UserNotification.objects.filter(recipient=request.user, unread=True):
            notification.unread = False
            notification.save()

    if request.is_ajax():
        return HttpResponse()

    if "HTTP_REFERER" in request.META:
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        return HttpResponseRedirect(reverse("home_index"))
