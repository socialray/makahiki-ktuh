"""Provide the view for the My_Achievements widget."""
from apps.widgets.smartgrid import  smartgrid


def supply(request, page_name):
    """Supply view_objects for the My_Achievements template."""
    _ = page_name
    user = request.user
    points_logs = user.pointstransaction_set.order_by("-transaction_date").all()

    return {
        "in_progress_members": smartgrid.get_in_progress_members(user),
        "points_logs": points_logs,
    }
