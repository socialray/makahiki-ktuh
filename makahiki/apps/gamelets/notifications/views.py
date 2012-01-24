from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect

from gamelets.notifications.models import UserNotification

def read(request, notification_id):
  if not request.method == "POST":
    raise Http404
    
  notification = get_object_or_404(UserNotification, pk=notification_id)
  notification.unread = False
  notification.save()
  if request.is_ajax():
    return HttpResponse()

  if request.META.has_key("HTTP_REFERER"):
    return HttpResponseRedirect(request.META["HTTP_REFERER"])
  else:
    return HttpResponseRedirect(reverse("home_index"))
    
    