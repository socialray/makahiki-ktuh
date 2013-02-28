"""badges module"""
from django.core.exceptions import ObjectDoesNotExist
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.player_mgr.models import Profile
from apps.utils import utils
from apps.widgets.badges.models import BadgeAward, Badge
from apps.managers.cache_mgr import cache_mgr


def get_badge(slug):
    """Returns the badge object."""
    try:
        return Badge.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return False


def award_badge(profile, badge):
    """award the badge to the user."""
    BadgeAward(profile=profile, badge=badge).save()
    if profile.team:
        cache_mgr.invalidate_template_cache("team_member_avatar", profile.team.id)


def award_possible_badges(profile, trigger):
    """Award any possible badges to a user.
    """
    if not challenge_mgr.is_game_enabled("Badge Game Mechanics"):
        return

    user_badges = []
    for awarded in profile.badgeaward_set.all().select_related("badge"):
        user_badges.append(awarded.badge)

    for badge in Badge.objects.filter(award_trigger=trigger):
        if not badge in user_badges and utils.eval_predicates(badge.award_condition, profile.user):
            award_badge(profile=profile, badge=badge)
            print "Awarded %s badge to %s." % (badge, profile)


def award_possible_daily_badges():
    """award badges for all users. called in an hourly scheduler."""
    if not challenge_mgr.is_game_enabled("Badge Game Mechanics"):
        return

    for p in Profile.objects.filter(setup_complete=True):
        award_possible_badges(p, "daily")
