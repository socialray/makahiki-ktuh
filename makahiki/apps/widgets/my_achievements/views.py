"""Provide the view for the My_Achievements widget."""
from apps.widgets.smartgrid import  get_in_progress_members


def supply(request, page_name):
    """Supply view_objects for the My_Achievements template."""
    _ = page_name
    user = request.user
    points_logs = user.pointstransaction_set.order_by("-submission_date").all()

    return {
        "in_progress_members": get_in_progress_members(user),
        "points_logs": points_logs,
    }
