"""handles request for referral status."""
from django.db.models.aggregates import Count
from apps.managers.player_mgr.models import Profile


def supply(request, page_name):
    """supply view_objects for user status."""
    _ = page_name
    _ = request

    # Find referrals.
    referrals = Profile.objects.filter(referring_user__isnull=False).values(
        'referring_user__profile__name', 'referring_user__username').annotate(
            referrals=Count('referring_user')
    )

    return {
        'referrals': referrals,
        }
