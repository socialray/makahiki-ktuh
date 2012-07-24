"""Handles request for prize status."""

from apps.managers.log_mgr.models import MakahikiLog


def supply(request, page_name):
    """supply view_objects for prize status."""
    _ = page_name
    _ = request

    entries = MakahikiLog.objects.all().order_by("-request_time")[:20]

    return {
        "entries": entries,
        }
