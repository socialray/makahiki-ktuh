"""
views handler for Badge widget rendering.
"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from apps.lib.brabeion.models import BadgeAward
from apps.lib.brabeion import badges
from apps.widgets.badges import user_badges


def supply(request, page_name):
    """ supply view_objects for widget rendering."""
    user = request.user
    _ = page_name

    # award possible badges,
    award_badges(user)

    return {}


def award_badges(user):
    """award possible badges.

    It could be useful to create a notification if any badge is awarded.
    which means the awarding part need to be in middleware for every page.
    """

    badges_slug = user_badges.DailyVisitorBadge.slug
    if user.badges_earned.filter(slug=badges_slug).count() == 0:
        badges.possibly_award_badge(badges_slug, user=user)

    badges_slug = user_badges.FullyCommittedBadge.slug
    if user.badges_earned.filter(slug=badges_slug).count() == 0:
        badges.possibly_award_badge(badges_slug, user=user)


@login_required
def badge_catalog(request):
    """handle the badge catelog request."""
    awarded_badges = [earned.badge for earned in request.user.badges_earned.all()]
    registry = badges.get_registry().copy()
    # Remove badges that are already earned
    for badge in awarded_badges:
        registry.pop(badge.slug)

    locked_badges = registry.values()

    # For each badge, get the number of people who have the badge.
    team = request.user.get_profile().team
    for badge in awarded_badges:
        badge.total_users = BadgeAward.objects.filter(slug=badge.slug).count()
        badge.team_users = User.objects.filter(badges_earned__slug=badge.slug,
            profile__team=team)
    for badge in locked_badges:
        badge.total_users = BadgeAward.objects.filter(slug=badge.slug).count()
        badge.team_users = User.objects.filter(badges_earned__slug=badge.slug,
            profile__team=team)

    return render_to_response("badge-catalog.html", {
        "awarded_badges": awarded_badges,
        "locked_badges": locked_badges,
        }, context_instance=RequestContext(request))
