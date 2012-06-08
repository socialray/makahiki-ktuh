"""badges module"""
from django.core.exceptions import ObjectDoesNotExist
from apps.widgets.badges.models import BadgeAward, Badge


def get_badge(slug):
    """Returns the badge object."""
    try:
        return Badge.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return False


def award_badge(user, badge):
    """award the badge to the user."""
    BadgeAward(user=user, badge=badge).save()
