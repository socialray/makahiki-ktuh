'''
Created on Jul 19, 2012

@author: Cam Moore
'''
from apps.widgets.badges.models import BadgeAward
from django.db.models.aggregates import Count


def supply(request, page_name):
    """supply the view objects for the badge status widget."""
    _ = page_name
    _ = request
    """
    badgeAward = {}
    for badge in Badge.objects.all():
        badgeAward[badge] = BadgeAward.objects.filter(badge=badge).count()
    badgeAward = sorted(badgeAward.items(), key=lambda x: -x[1])
    badges = Badge.objects.all()
    """
    return {
        "badge_awards": BadgeAward.objects.values(
            'badge__name', 'badge__theme', 'badge__label').annotate(
            count=Count('badge')).order_by('-count'),
    }
