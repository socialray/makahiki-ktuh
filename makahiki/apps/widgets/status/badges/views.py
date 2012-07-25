'''
Created on Jul 19, 2012

@author: Cam Moore
'''
from apps.widgets.badges.models import Badge, BadgeAward


def supply(request, page_name):
    """supply the view objects for the badge status widget."""
    _ = page_name
    _ = request
    badgeAward = {}
    for badge in Badge.objects.all():
        badgeAward[badge] = BadgeAward.objects.filter(badge=badge).count()
    badgeAward = sorted(badgeAward.items(), key=lambda x: -x[1])
    badges = Badge.objects.all()
    return {
            "badge_awards": badgeAward,
            "badges": badges,
            }
