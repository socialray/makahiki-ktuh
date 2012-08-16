"""badges module"""
from django.core.exceptions import ObjectDoesNotExist
from apps.managers.player_mgr.models import Profile
from apps.utils import utils
from apps.widgets.badges.models import BadgeAward, Badge


def get_badge(slug):
    """Returns the badge object."""
    try:
        return Badge.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return False


def award_badge(profile, badge):
    """award the badge to the user."""
    BadgeAward(profile=profile, badge=badge).save()


def award_possible_badges(profile):
    """Award any possible badges to a user.
    """
    user_badges = []
    for awarded in profile.badgeaward_set.all().select_related():
        user_badges.append(awarded.badge)

    for badge in Badge.objects.all():
        if not badge in user_badges and utils.eval_predicates(badge.award_condition, profile.user):
            award_badge(profile=profile, badge=badge)


def award_badges():
    """award badges for all users. called in an hourly scheduler."""
    for p in Profile.objects.filter(setup_completed=True):
        award_possible_badges(p.user)
