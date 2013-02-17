"""badge model."""
from django.db import models
from datetime import datetime
from django.conf import settings
from apps.managers.player_mgr.models import Profile
from apps.widgets.notifications.models import UserNotification
from apps.utils.utils import media_file_path


_MEDIA_LOCATION = "badges"
"""location for uploaded files."""


class Badge(models.Model):
    """Defines Badge model."""
    THEME_CHOICES = (
                     ('1', "theme 1"),
                     ('2', "theme 2"),
                     ('3', "theme 3"),
                     ('4', "theme 4"),
                     ('5', "theme 5"),
                     )
    TRIGGER_CHOICES = (('daily', 'daily'),
                       ('smartgrid', 'smartgrid'),
                      )
    name = models.CharField(max_length=255,
                            help_text="The name of the badge")
    label = models.CharField(max_length=20,
                            help_text="The label of the badge")
    description = models.CharField(max_length=255,
                                   help_text="The description of the badge")
    hint = models.CharField(max_length=255,
                            help_text="The Hint of the badge")
    slug = models.CharField(max_length=255,
                            help_text="A unique identifier of the badge. Automatically generated "
                                      "if left blank.")
    image = models.ImageField(
        max_length=255, blank=True, null=True,
        upload_to=media_file_path(_MEDIA_LOCATION),
        help_text="The image of the badge.",)
    award_condition = models.CharField(
        max_length=1024,
        help_text="if the condition is True, the badge will be awarded. " +
                   settings.PREDICATE_DOC_TEXT)

    award_trigger = models.CharField(max_length=10, choices=TRIGGER_CHOICES, default='daily',
                                     help_text="The trigger of evaluating the award condition.")

    theme = models.CharField(max_length=1, choices=THEME_CHOICES, default='6',
                             help_text="The theme for the badge.")
    points = models.IntegerField(
        default=0,
        help_text="Points awarded for getting badge."
    )

    priority = models.IntegerField(
        default=0,
        help_text="sorting order in the badge list, lower value (higher priority) appears first."
    )
    admin_tool_tip = "Player Badges"

    def __unicode__(self):
        return self.name


class BadgeAward(models.Model):
    """Defines model for awarded badge."""
    profile = models.ForeignKey(Profile)
    badge = models.ForeignKey(Badge)
    awarded_at = models.DateTimeField(default=datetime.now)
    admin_tool_tip = "Awarded Badges"

    def save(self, *args, **kwargs):
        """custom save method."""

        message = "Congratulations, You have been awarded the {0} badge. ".format(self.badge.name)
        message += "<div class=\"badge-theme-{0}-small\"><p>{1}</p></div>".format(self.badge.theme,
                                                                                  self.badge.label)
        message += "Check out your badges <a href= %s >here</a>" % "/profile/?ref=dialog"
        UserNotification.create_info_notification(
            self.profile.user,
            message,
            True,
            content_object=self
        )

        message = "Badge: %s" % self.badge.name
        self.profile.add_points(self.badge.points, self.awarded_at, message, self)
        super(BadgeAward, self).save(args, kwargs)
