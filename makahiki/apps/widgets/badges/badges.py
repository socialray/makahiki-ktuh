"""badges module"""
from django.core.exceptions import ObjectDoesNotExist
from apps.utils import utils
from apps.widgets.badges.models import BadgeAward, Badge


def get_badge(slug):
    """Returns the badge object."""
    try:
        return Badge.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return False


def award_badge(user, badge):
    """award the badge to the user."""
    BadgeAward(profile=user.get_profile(), badge=badge).save()


def award_possible_badges(user):
    """Award any possible badges to a user.
    """
    for badge in Badge.objects.all():
        if not BadgeAward.objects.filter(badge=badge, profile=user.get_profile()) and \
           utils.eval_predicates(badge.award_condition, user):
            award_badge(user=user, badge=badge)
