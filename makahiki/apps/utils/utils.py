"""Provides common utility functions."""
from django.conf import settings
import os


def media_file_path(prefix=None):
    """return the path for the media file."""
    if prefix:
        return os.path.join(settings.MAKAHIKI_MEDIA_PREFIX, prefix)
    else:
        return settings.MAKAHIKI_MEDIA_PREFIX


def get_smartgrid_predicates():
    """Returns the predicates defined in smartgrid module."""
    from apps.widgets.smartgrid.predicates import completed_action, approved_action, \
        completed_some_of, completed_all_of, approved_all_of, approved_some_of
    return {
            "completed_action": completed_action,
            "completed_some_of": completed_some_of,
            "completed_all_of": completed_all_of,
            "approved_action": approved_action,
            "approved_some_of": approved_some_of,
            "approved_all_of": approved_all_of,
            }


def get_player_mgr_predicates():
    """Returns the predicates defined in player_mgr module."""
    from apps.managers.player_mgr.predicates import badge_awarded, posted_to_wall, \
        set_profile_pic, has_points, is_admin, allocated_ticket, daily_visit_count
    return {
        "is_admin": is_admin,
        "has_points": has_points,
        "allocated_ticket": allocated_ticket,
        "badge_awarded": badge_awarded,
        "posted_to_wall": posted_to_wall,
        "set_profile_pic": set_profile_pic,
        "daily_visit_count": daily_visit_count,
        }


def eval_predicates(predicates, user):
    """Returns the boolean evaluation result of the predicates against the user."""

    user_predicates = predicates.replace("(", "(user,")

    allow_dict = {"True": True, "False": False, "user": user}
    allow_dict.update(get_player_mgr_predicates())
    allow_dict.update(get_smartgrid_predicates())

    return eval(user_predicates, {"__builtins__": None}, allow_dict)
