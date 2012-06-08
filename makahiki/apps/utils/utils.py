"""Provides common utility functions."""
from django.conf import settings
import os

def media_file_path(prefix=None):
    """return the path for the media file."""
    if prefix:
        return os.path.join(settings.MAKAHIKI_MEDIA_PREFIX, prefix)
    else:
        return settings.MAKAHIKI_MEDIA_PREFIX


def eval_predicates(predicates, user):
    """Returns the boolean evaluation result of the predicates against the user."""

    user_predicates = predicates.replace("(", "(user,")

    from apps.managers.player_mgr.predicates import badge_awarded, posted_to_wall, set_profile_pic,\
        has_points, is_admin, allocated_ticket
    from apps.widgets.smartgrid.predicates import completed_action, action_approved


    ALLOW_PREDICATES_DICT = {
        "completed_action": completed_action,
        "action_approved": action_approved,
        "is_admin": is_admin,
        "has_points": has_points,
        "allocated_ticket": allocated_ticket,
        "badge_awarded": badge_awarded,
        "posted_to_wall": posted_to_wall,
        "set_profile_pic": set_profile_pic,
    }

    allow_dict = ALLOW_PREDICATES_DICT.copy()
    allow_dict.update({"True": True, "False": False, "user": user})

    return eval(user_predicates, {"__builtins__": None}, allow_dict)
