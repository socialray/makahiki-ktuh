"""handles request for iframe widget."""


def supply(request, page_name):
    """supply view_objects for user status."""
    _ = page_name
    _ = request

    default_url = "/home"
    return {
        "default_url": default_url
        }
