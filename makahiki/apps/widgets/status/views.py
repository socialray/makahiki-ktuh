"""Provides the view of a help topic."""
from django.http import HttpResponse
from apps.widgets.status.analysis import calculate_summary_stats, calculate_action_stats, \
    calculate_user_stats


def supply(request, page_name):
    """ supply view_objects for widget rendering."""

    _ = request
    _ = page_name

    return {}


def analysis(request):
    """analysis"""
    _ = request

    message = calculate_summary_stats()
    message += calculate_action_stats()
    message += calculate_user_stats()

    return HttpResponse(message, content_type="text", mimetype='text/plain')
