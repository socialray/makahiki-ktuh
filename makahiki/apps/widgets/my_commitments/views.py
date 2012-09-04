"""Provide the view for the My_Commitments widget."""
from apps.widgets.smartgrid import  smartgrid


def supply(request, page_name):
    """Supply view_objects contents, which are the commitment members."""
    _ = page_name
    # Get the user's current commitments.
    commitment_members = smartgrid.get_current_commitment_members(request.user)
    return {
        "commitment_members": commitment_members,
        }
