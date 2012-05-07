"""Provides common utility functions."""
from django.conf import settings
import os


def media_file_path(prefix=None):
    """return the path for the media file."""
    if prefix:
        return os.path.join(settings.MAKAHIKI_MEDIA_PREFIX, prefix)
    else:
        return settings.MAKAHIKI_MEDIA_PREFIX


def eval_predicates(predicates, user, allowed_predicates):
    """Returns the boolean evaluation result of the predicates against the user."""
    user_predicates = predicates

    for name in allowed_predicates.keys():
        user_predicates = user_predicates.replace(name + "(", name + "(user,")

    allow_dict = allowed_predicates.copy()
    allow_dict.update({"True": True, "False": False, "user": user})

    return eval(user_predicates, {"__builtins__": None}, allow_dict)
