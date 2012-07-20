'''
Created on Jul 19, 2012

@author: Cam Moore
'''
from apps.managers.player_mgr.models import Profile
from django.db.models.aggregates import Count


def supply(request, page_name):
    """supply the view objects for the badge status widget."""
    _ = page_name
    _ = request
    profiles_with_badges = Profile.objects.annotate(num_badges=Count('badgeaward'))\
        .order_by('-num_badges').filter(num_badges__gt=0)
    return {
            "profiles": profiles_with_badges
            }
