"""Defines the model containing game settings."""
import datetime
from django.conf import settings
from django.db import models
from apps.managers.cache_mgr import cache_mgr
from apps.utils.utils import media_file_path


_MEDIA_LOCATION = "challenge"
"""location for challenge files."""

_MEDIA_LOCATION_UPLOAD = "uploads"
"""location for uploaded files."""


class ChallengeSetting(models.Model):
    """Defines the global settings for the challenge."""

    THEME_CHOICES = ((key, key) for key in settings.INSTALLED_THEMES)

    domain = models.CharField(
        default="localhost",
        help_text="The domain name of this challenge.",
        max_length=100,)
    logo = models.ImageField(
        upload_to=media_file_path(_MEDIA_LOCATION),
        max_length=255, blank=True, null=True,
        help_text="The logo of the challenge.",)
    name = models.CharField(
        default="Kukui Cup",
        help_text="The name of the challenge.",
        max_length=50,)
    theme = models.CharField(
        default="theme-forest",
        help_text="The default theme for this challenge.",
        choices=THEME_CHOICES,
        max_length=50,)
    team_label = models.CharField(
        default="Team",
        help_text="The display label for 'teams'.",
        max_length=50,)

    # CAS settings
    use_cas_auth = models.BooleanField(
        default=False,
        help_text="Use CAS authentication ?")
    cas_server_url = models.CharField(
        null=True, blank=True,
        help_text="The URL for CAS authentication service. " \
                  "Example: https://login.its.hawaii.edu/cas/",
        max_length=100,)
    cas_auth_text = models.TextField(
        default="###I have a CAS email",
        help_text="A button will appear if there is other auth method(s) selected. "
                  "This is the text for the CAS auth button. " + settings.MARKDOWN_TEXT,
        max_length=255,)

    # LDAP settings
    use_ldap_auth = models.BooleanField(
        default=False,
        help_text="Use LDAP authentication ?")
    ldap_server_url = models.CharField(
        null=True, blank=True,
        help_text="The URL for LDAP authentication service. Example: ldap://localhost:10389",
        max_length=100,)
    ldap_search_base = models.CharField(
        null=True, blank=True,
        help_text="The search base for the ldap service. Example: ou=users,ou=system",
        max_length=100,)
    ldap_auth_text = models.TextField(
        default="###I have a LDAP email",
        help_text="A button will appear if there is other auth method(s) selected. "
                  "This is the text for the LDAP auth button. " + settings.MARKDOWN_TEXT,
        max_length=255,)

    # internal authentication
    use_internal_auth = models.BooleanField(
        default=False,
        help_text="Use internal authentication ?")
    internal_auth_text = models.TextField(
        default="###Others",
        help_text="A button will appear if there is other auth method(s) selected. "
                  "This is the text for the internal auth button. " + settings.MARKDOWN_TEXT,
        max_length=255,)

    # Wattdepot server
    wattdepot_server_url = models.CharField(
        null=True, blank=True,
        help_text="The URL for Wattdepot service. " \
                  "Example: http://localhost:8194/wattdepot",
        max_length=100,)

    # email settings
    email_enabled = models.BooleanField(
        default=False,
        help_text="Enable email ?",
        )
    contact_email = models.CharField(
        default="CHANGEME@example.com",
        help_text="The contact email of the admin.",
        max_length=100,)
    email_host = models.CharField(
        null=True, blank=True,
        help_text="The host name of the email server.",
        max_length=100,)
    email_port = models.IntegerField(
        default=587,
        help_text="The port of the email server",)
    email_use_tls = models.BooleanField(
        default=True,
        help_text="Use TLS in the email server ?",)

    # landing page content settings
    landing_slogan = models.TextField(
        default="The Kukui Cup: Lights off, game on!",
        help_text="The slogan text in the landing page. " + settings.MARKDOWN_TEXT,
        max_length=255,)
    landing_introduction = models.TextField(
        default="Aloha! Welcome to the Kukui Cup.",
        help_text="The introduction in the landing page. " + settings.MARKDOWN_TEXT,
        max_length=500,)
    landing_participant_text = models.TextField(
        default="###I am registered",
        max_length=255,
        help_text="The text of the participant button in the landing page. " +
                  settings.MARKDOWN_TEXT)
    landing_non_participant_text = models.TextField(
        default="###I am not registered.",
        max_length=255,
        help_text="The text of the non participant button in the landing page. " +
                  settings.MARKDOWN_TEXT)

    admin_tool_tip = "The global settings for the challenge. (Name, landing page, " + \
    "about page, and sponsors)"

    class Meta:
        """meta"""
        verbose_name = "global setting"

    def __unicode__(self):
        return self.name

    def is_multi_auth(self):
        """returns true if use_cas and either use ldap or internal."""
        if self.use_cas_auth:
            if self.use_ldap_auth or self.use_internal_auth:
                return True
        elif self.use_ldap_auth and self.use_internal_auth:
            return True
        return False

    def round_info(self):
        """returns the info for all rounds."""
        return settings.COMPETITION_ROUNDS

    def about_page_text(self):
        """returns the about page text."""
        aboutpage, _ = AboutPage.objects.get_or_create(pk=1)
        return aboutpage.about_page_text

    def save(self, *args, **kwargs):
        """Custom save method."""
        super(ChallengeSetting, self).save(*args, **kwargs)
        cache_mgr.delete("challenge")


class UploadImage(models.Model):
    """Defines the table for uploaded images."""
    image = models.ImageField(
        upload_to=media_file_path(_MEDIA_LOCATION_UPLOAD),
        max_length=255, blank=True, null=True,
        help_text="The uploaded image.",)

    def __unicode__(self):
        return self.image.name


class AboutPage(models.Model):
    """Defines the sponsor for this challenge."""
    challenge = models.ForeignKey("ChallengeSetting")
    about_page_text = models.TextField(
        default="For more information, please go to " \
                "<a href='http://kukuicup.org'>kukuicup.org</a>.",
        help_text="The text of the about page that explains the challenge. " +
                  settings.MARKDOWN_TEXT)

    class Meta:
        """meta"""
        verbose_name = "about page"
        verbose_name_plural = "about page"

    def __unicode__(self):
        return ""


class Sponsor(models.Model):
    """Defines the sponsor for this challenge."""
    challenge = models.ForeignKey("ChallengeSetting")

    priority = models.IntegerField(
        default="1",
        help_text="The priority of the sponsor")
    name = models.CharField(
        help_text="The name of the sponsor.",
        max_length=200,)
    url = models.CharField(
        help_text="The url of the sponsor.",
        max_length=200,)
    logo_url = models.CharField(
        blank=True, null=True,
        help_text="The url of the sponsor logo.",
        max_length=200,)
    logo = models.ImageField(
        upload_to=media_file_path(_MEDIA_LOCATION),
        max_length=255, blank=True, null=True,
        help_text="The logo of the sponsor.",)

    class Meta:
        """meta"""
        ordering = ['priority', 'name', ]

    def __unicode__(self):
        return ""


class RoundSetting(models.Model):
    """Defines the round settings for this challenge."""

    """Start means the competition will start at midnight on that date.
    End means the competition will end at one minute to midnight on the previous day.
    For example, a round that ends on "2010-08-02" will end at 11:59pm of August 1st.
    """
    name = models.CharField(
        default="Round 1",
        help_text="The name of the round.",
        max_length=50,)
    start = models.DateTimeField(
        default=datetime.datetime.today(),
        help_text="The start date of the round.")
    end = models.DateTimeField(
        default=datetime.datetime.today() + datetime.timedelta(7),
        help_text="The end date of the round.")
    round_reset = models.BooleanField(
        default=False,
        help_text="Reset the points for this round? if reset, the points from previous round"
                  "will not be carried over to this round."
    )
    display_scoreboard = models.BooleanField(
        default=True,
        help_text="Display the round in scoreboard?"
    )
    admin_tool_tip = "The Round information for the challenge. (How many, when, etc.)"

    class Meta:
        """Meta"""
        ordering = ['start']
        unique_together = ("name", )

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Custom save method."""
        super(RoundSetting, self).save(*args, **kwargs)
        cache_mgr.delete("rounds")


class PageInfo(models.Model):
    """Defines the page info."""
    name = models.CharField(
        help_text="The name of the page. It is used to determine which navbar icon is used.",
        max_length=50,)
    label = models.CharField(
        help_text="The label of the page. It is used on the Home page and the navbar. " + \
        "</br>Should be less than 10 characters long.",
        max_length=100,)
    title = models.CharField(
        blank=True, null=True,
        help_text="The HTML title of the page.",
        max_length=255,)
    introduction = models.TextField(
        blank=True, null=True,
        help_text="This text is shown on the Home page. It should not be more than 3 lines," + \
        "</br>each line should be less than 25 characters long. " + settings.MARKDOWN_TEXT,
        max_length=1000,)
    priority = models.IntegerField(
        default=1,
        help_text="The priority (ordering) of the page.")
    url = models.CharField(
        default="/",
        help_text="The URL of the page.",
        max_length=255,)
    unlock_condition = models.CharField(
        default="True",
        max_length=255,
        help_text="if the condition is True, the page will be unlocked. " +
                  settings.PREDICATE_DOC_TEXT)
    admin_tool_tip = "The top level page information. Defines which widgets " + \
    "are on the page, if the page is displayed, and the ordering of the pages."

    class Meta:
        """meta"""
        ordering = ['priority', ]

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Custom save method."""
        super(PageInfo, self).save(*args, **kwargs)
        cache_mgr.clear()


class PageSetting(models.Model):
    """Defines widgets in a page."""
    WIDGET_CHOICES = ((key, key) for key in settings.INSTALLED_WIDGET_APPS)
    LOCATION_CHOICES = (("Left", "Left"),
                        ("Right", "Right"))

    page = models.ForeignKey("PageInfo")

    widget = models.CharField(
        blank=True, null=True,
        help_text="The name of the widget in the page.",
        choices=WIDGET_CHOICES,
        max_length=50,)

    location = models.CharField(
        default="Left",
        blank=True, null=True,
        help_text="The location of the widget in the page.",
        choices=LOCATION_CHOICES,
        max_length=10,)

    priority = models.IntegerField(
        default=1,
        help_text="The priority (ordering) of widget in the location of the page.")

    enabled = models.BooleanField(
        default=True,
        help_text="Enable ?",)

    class Meta:
        """meta"""
        unique_together = (("page", "widget", ), )
        ordering = ['page', 'location', 'priority']
        verbose_name = "page widget"

    def __unicode__(self):
        return ""

    def save(self, *args, **kwargs):
        """Custom save method."""
        super(PageSetting, self).save(*args, **kwargs)
        cache_mgr.clear()


class GameInfo(models.Model):
    """Defines the game info."""
    name = models.CharField(
        help_text="The name of the game.",
        max_length=50,)
    enabled = models.BooleanField(
        default=True,
        help_text="Enable ?",)
    priority = models.IntegerField(
        default=1,
        help_text="The priority (ordering) of the game in the admin interface.")

    class Meta:
        """meta"""
        ordering = ['priority', ]

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Custom save method."""
        super(GameInfo, self).save(*args, **kwargs)
        cache_mgr.clear()


class GameSetting(models.Model):
    """Defines the widgets in a game."""
    WIDGET_CHOICES = ((key, key) for key in settings.INSTALLED_WIDGET_APPS)

    game = models.ForeignKey("GameInfo")

    widget = models.CharField(
        help_text="The name of the widget in the page.",
        choices=WIDGET_CHOICES,
        max_length=50,)

    class Meta:
        """meta"""
        unique_together = (("game", "widget", ), )
        ordering = ['game', 'widget', ]

    def __unicode__(self):
        return ""

    def save(self, *args, **kwargs):
        """Custom save method."""
        super(GameSetting, self).save(*args, **kwargs)
        cache_mgr.clear()
