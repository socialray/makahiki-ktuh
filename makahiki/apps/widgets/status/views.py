"""Provides the view of a help topic."""
from django.http import HttpResponse
from apps.widgets.status import analysis


def supply(request, page_name):
    """ supply view_objects for widget rendering."""

    _ = request
    _ = page_name

    return {}


def analysis_view(request, command):
    """analysis"""
    _ = request

    if command == "summary":
        result = analysis.calculate_summary_stats()
    elif command == "actions":
        result = analysis.calculate_action_stats()
    elif command == "users":
        result = analysis.calculate_user_stats()
    elif command == "user_summary":
        users = request.GET.get("user", "")
        result = analysis.calculate_user_summary(users)
    elif command == "timestamps":
        team = request.GET.get("team", "")
        date_start = request.GET.get("date_start", "")
        date_end = request.GET.get("date_end", "")
        result = analysis.user_timestamps(team, date_start, date_end)
    else:
        result = "please specify an analysis command."

    return HttpResponse(result, content_type="text", mimetype='text/plain')
