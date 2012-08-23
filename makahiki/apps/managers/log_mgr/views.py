"""Support logging of AJAX-based interactions."""
from django.http import Http404, HttpResponse


def log_ajax(request, obj_type, obj, action):
    """Simple AJAX view provided to support logging actions.

    Note that since the logger intercepts requests and responses,
    this method just returns a success response.
    """
    _ = obj_type
    _ = obj
    _ = action
    if request.is_ajax() and request.method == "GET":
        return HttpResponse()

    raise Http404
