"""Provide the view for the My_Commitments widget."""
from apps.widgets.smartgrid import  get_current_commitment_members


def supply(request, page_name):
    """Supply view_objects contents, which are the commitment members."""
    _ = page_name
    # Get the user's current commitments.
    commitment_members = get_current_commitment_members(request.user).select_related("commitment")

    return {
        "commitment_members": commitment_members,
        }
