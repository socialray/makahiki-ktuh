"""Handle the rendering of the water goal widget."""
from apps.widgets.resource_goal.views import resource_supply


def supply(request, page_name):
    """Supply the view_objects content."""
    _ = request
    _ = page_name
    return resource_supply(request, "water")
