"""Handle the rendering of the energy scoreboard widget."""
from apps.widgets.resource_scoreboard.views import resource_supply


def supply(request, page_name):
    """Supply the view_objects content."""
    _ = request
    _ = page_name
    return resource_supply(request, "energy")
