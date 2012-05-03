"""Provides common utility functions."""
from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage


def media_file_path(prefix=None):
    """return the path for the media file."""
    if prefix:
        return os.path.join(settings.MAKAHIKI_MEDIA_PREFIX, prefix)
    else:
        return settings.MAKAHIKI_MEDIA_PREFIX


class OverwriteStorage(FileSystemStorage):
    """overwrite the default file upload behavior to overwrite the file if same.
    ref: http://djangosnippets.org/snippets/976/
    usage:
    use storage=OverwriteStorage() on your FileField declarations.
    example, a_file = models.FileField(upload_to="/", storage=OverwriteStorage(), blank=True)
    """
    def get_available_name(self, name):
        """
        Returns a filename that's free on the target storage system, and
        available for new content to be written to.
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            self.delete(name)
        return name


def eval_predicates(predicates, user, allowed_predicates):
    """Returns the boolean evaluation result of the predicates against the user."""
    user_predicates = predicates

    for name in allowed_predicates.keys():
        user_predicates = user_predicates.replace(name + "(", name + "(user,")

    allow_dict = allowed_predicates.copy()
    allow_dict.update({"True": True, "False": False, "user": user})

    return eval(user_predicates, {"__builtins__": None}, allow_dict)
