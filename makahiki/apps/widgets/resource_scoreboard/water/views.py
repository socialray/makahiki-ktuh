"""Handle the rendering of the energy scoreboard widget."""
from apps.widgets.resource_scoreboard.views import resource_supply


def supply(request, page_name):
    """Supply the view_objects content."""
    _ = request

    view_objects = resource_supply(request, "water", page_name)
    view_objects["no_carousel"] = (page_name == "status")
    return view_objects
