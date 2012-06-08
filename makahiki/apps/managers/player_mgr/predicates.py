"""Provides predicate functions for runtime condition evaluation."""

def has_points(user, points):
    """Returns True if the user has more than the specified points."""
    return user.get_profile().points() >= points


def is_admin(user):
    """Returns True if the user is an admin."""
    return user.is_staff or user.is_superuser

def allocated_ticket(user):
    """Returns True if the user has any allocated tickets."""
    return user.raffleticket_set.count() > 0


def badge_awarded(user, badge_slug):
    """Returns True if the badge is awarded to the user."""
    for badge in user.badges_earned.all():
        if badge.slug == badge_slug:
            return True

    return False


def posted_to_wall(user):
    """Returns True if the user posted to their wall and False otherwise."""
    if user.post_set.filter(style_class="user_post").count() > 0:
        return True
    return False


def set_profile_pic(user):
    """Returns True if the user posted to their wall and False otherwise."""
    if user.avatar_set.filter(primary=True).count() > 0:
        return True
    return False

