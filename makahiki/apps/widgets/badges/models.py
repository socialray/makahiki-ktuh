"""badge model."""

from datetime import datetime

from django.db import models

from django.contrib.auth.models import User
from apps.utils.utils import media_file_path


_MEDIA_LOCATION = "badges"
"""location for uploaded files."""


class Badge(models.Model):
    """Defines Badge model."""
    name = models.CharField(max_length=255,
                            help_text="The name of the badge")
    label = models.CharField(max_length=20,
                            help_text="The label of the badge")
    description = models.CharField(max_length=255,
                                   help_text="The description of the badge")
    hint = models.CharField(max_length=255,
                            help_text="The Hint of the badge")
    slug = models.CharField(max_length=255,
                            help_text="Automatically generated if left blank.")
    image = models.ImageField(
        max_length=255, blank=True, null=True,
        upload_to=media_file_path(_MEDIA_LOCATION),
        help_text="The image of the badge.",)
    award_condition = models.CharField(max_length=1024,
                                       help_text="If the condition is true, the badge is awarded.")

    def __unicode__(self):
        return self.name


class BadgeAward(models.Model):
    """Defines model for awarded badge."""
    user = models.ForeignKey(User)
    badge = models.ForeignKey(Badge)
    awarded_at = models.DateTimeField(default=datetime.now)
