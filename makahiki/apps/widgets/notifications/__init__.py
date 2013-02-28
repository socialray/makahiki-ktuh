"""Provides the notification service."""
import re
from apps.managers.cache_mgr import cache_mgr
from django.conf import settings

from apps.widgets.notifications.models import UserNotification


def _strip_html_tag(contents):
    """strip the html tag."""
    p = re.compile(r'<.*?>')
    return p.sub('', contents)


def get_unread_notifications(user, limit=None):
    """Retrieves the user's unread notifications that are to be displayed on the web.
       Returns a dictionary containing their alerts, their unread notifications, and if there are
       more unread notifications."""

    if not user:
        return None

    notifications = cache_mgr.get_cache("notification-%s" % user.username)
    if notifications is None:

        notifications = {"has_more": False,
                         "use_facebook": settings.MAKAHIKI_USE_FACEBOOK}

        # Find undisplayed alert notifications.
        notifications.update({"alerts": get_user_alert_notifications(user)})

        # Get unread notifications
        unread_notifications = user.usernotification_set.filter(
            unread=True,).order_by("-level", "-created_at")
        if limit:
            if unread_notifications.count() > limit:
                notifications.update({"has_more": True})
            unread_notifications = unread_notifications[:limit]

        for item in unread_notifications:
            item.fb_contents = _strip_html_tag(item.contents)
        notifications.update({"unread": unread_notifications})

        cache_mgr.set_cache("notification-%s" % user.username, notifications, 1800)
    return notifications


def get_unread_count(user):
    """Get the number of notifications that are unread."""
    return UserNotification.objects.filter(recipient=user, unread=True).count()


def get_user_alert_notifications(user):
    """Retrieves notifications that should be displayed in an alert."""
    notifications = user.usernotification_set.filter(
        unread=True,
        display_alert=True,
    ).order_by("-level", "-created_at")

    for item in notifications:
        item.fb_contents = _strip_html_tag(item.contents)

    return notifications
