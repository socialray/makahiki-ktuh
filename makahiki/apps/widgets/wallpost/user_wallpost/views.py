"""Handles wall post widget request and rendering."""

from django.contrib.auth.decorators import login_required
from apps.widgets.wallpost.views import super_supply, super_more_posts


def supply(request, page_name):
    """supply the view_objects."""
    return super_supply(request, page_name, "user")


@login_required
def more_posts(request):
    """handle more post link"""
    return super_more_posts(request, "user")
