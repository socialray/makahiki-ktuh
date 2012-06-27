"""Power meters visualization."""

from apps.widgets.viz_power_meters.views import remote_supply


def supply(request, page_name):
    """ Call the remote viz request."""

    _ = page_name
    _ = request

    return remote_supply(request, page_name)
