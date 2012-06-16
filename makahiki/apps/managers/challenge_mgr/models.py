"""Defines the model containing game settings."""
import datetime
from django.conf import settings
from django.db import models
from apps.utils.utils import media_file_path


_MEDIA_LOCATION = "challenge"
"""location for challenge files."""

_MEDIA_LOCATION_UPLOAD = "uploads"
"""location for uploaded files."""


class ChallengeSetting(models.Model):
    """Defines the global settings for the challenge."""

    THEME_CHOICES = ((key, key) for key in settings.INSTALLED_THEMES)

    site_name = models.CharField(
        default="My site",
        help_text="The name of the site.",
        max_length=50,)
    site_domain = models.CharField(
        default="localhost",
        help_text="The domain name of the site.",
        max_length=100,)
    site_logo = models.ImageField(
        upload_to=media_file_path(_MEDIA_LOCATION),
        max_length=255, blank=True, null=True,
        help_text="The logo of the site.",)
    competition_name = models.CharField(
        default="Kukui Cup",
        help_text="The name of the competition.",
        max_length=50,)
    theme = models.CharField(
        default="theme-forest",
        help_text="The UI theme for this installation.",
        choices=THEME_CHOICES,
        max_length=50,)
    competition_team_label = models.CharField(
        default="Team",
        help_text="The display label for team.",
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
        help_text="The CAS login button text in the landing page. " + settings.MARKDOWN_TEXT,
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
        help_text="The LDAP login button text in the landing page. " + settings.MARKDOWN_TEXT,
        max_length=255,)

    # internal authentication
    use_internal_auth = models.BooleanField(
        default=False,
        help_text="Use internal authentication ?")
    internal_auth_text = models.TextField(
        default="###Others",
        help_text="The internal login button text in the landing page. " + settings.MARKDOWN_TEXT,
        max_length=255,)

    # Wattdepot server
    wattdepot_server_url = models.CharField(
        null=True, blank=True,
        help_text="The URL for Wattdepot service. " \
                  "Example: http://localhost:<port>",
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

    about_page_text = models.TextField(
        default="For more information, please go to " \
                "<a href='http://kukuicup.org'>kukuicup.org</a>.",
        help_text="The text of the about page. " +
                  settings.MARKDOWN_TEXT)

    def __unicode__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        """Custom save method."""
        super(ChallengeSetting, self).save(*args, **kwargs)
        ChallengeSetting.set_settings()

    @staticmethod
    def set_settings():
        """get the CALLENGE setting from DB and set the global django settings."""
        settings.CHALLENGE, _ = ChallengeSetting.objects.get_or_create(pk=1)

        # email settings
        if settings.CHALLENGE.email_enabled:
            settings.SERVER_EMAIL = settings.CHALLENGE.contact_email
            settings.EMAIL_HOST = settings.CHALLENGE.email_host
            settings.EMAIL_PORT = settings.CHALLENGE.email_port
            settings.EMAIL_USE_TLS = settings.CHALLENGE.email_use_tls
            settings.ADMINS = (('Admin', settings.CHALLENGE.contact_email),)

        # set the is_multi_auth to true if use_cas and either use ldap or internal
        settings.CHALLENGE.is_multi_auth = False
        if settings.CHALLENGE.use_cas_auth:
            if settings.CHALLENGE.use_ldap_auth or settings.CHALLENGE.use_internal_auth:
                settings.CHALLENGE.is_multi_auth = True
        elif settings.CHALLENGE.use_ldap_auth and settings.CHALLENGE.use_internal_auth:
            settings.CHALLENGE.is_multi_auth = True

        # setting for the CAS authentication service.
        if settings.CHALLENGE.cas_server_url:
            settings.CAS_SERVER_URL = settings.CHALLENGE.cas_server_url
            settings.CAS_REDIRECT_URL = '/'
            settings.CAS_IGNORE_REFERER = True

        # ldap settings
        if settings.CHALLENGE.ldap_server_url:
            from django_auth_ldap.config import LDAPSearch
            import ldap

            settings.AUTH_LDAP_SERVER_URI = settings.CHALLENGE.ldap_server_url
            settings.AUTH_LDAP_USER_SEARCH = LDAPSearch("%s" % settings.CHALLENGE.ldap_search_base,
                                               ldap.SCOPE_SUBTREE, "(uid=%(user)s)")


class UploadImage(models.Model):
    """Defines the global settings for the challenge."""
    image = models.ImageField(
        upload_to=media_file_path(_MEDIA_LOCATION_UPLOAD),
        max_length=255, blank=True, null=True,
        help_text="The uploaded image.",)

    def __unicode__(self):
        return self.image.name


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
        return self.name


class RoundSetting(models.Model):
    """Defines the round settings for this challenge.

    Start means the competition will start at midnight on that date.
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

    class Meta:
        """Meta"""
        ordering = ['start']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Custom save method."""
        super(RoundSetting, self).save(*args, **kwargs)
        RoundSetting.set_settings()

    @staticmethod
    def set_settings():
        """set the round info in the system settings."""
        rounds = RoundSetting.objects.all()
        if not rounds:
            RoundSetting.objects.create()
            rounds = RoundSetting.objects.all()

        #store in a round dictionary and calculate start and end
        rounds_dict = {}
        settings.COMPETITION_START = None
        last_round = None
        for r in rounds:
            if settings.COMPETITION_START is None:
                settings.COMPETITION_START = r.start
            rounds_dict[r.name] = {
                "start": r.start,
                "end": r.end, }
            last_round = r
        if last_round:
            settings.COMPETITION_END = last_round.end
        settings.COMPETITION_ROUNDS = rounds_dict


class PageInfo(models.Model):
    """Defines the page info."""
    name = models.CharField(
        help_text="The name of the page.",
        max_length=50,)
    label = models.CharField(
        help_text="The label of the page.",
        max_length=100,)
    title = models.CharField(
        blank=True, null=True,
        help_text="The title of the page.",
        max_length=255,)
    introduction = models.TextField(
        blank=True, null=True,
        help_text="The introduction of the page. " + settings.MARKDOWN_TEXT,
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
        help_text="The conditions string to unlock the page.",)

    class Meta:
        """meta"""
        ordering = ['priority', ]

    def __unicode__(self):
        return self.name


class PageSetting(models.Model):
    """Defines widgets in a page."""
    WIDGET_CHOICES = ((key, key) for key in settings.INSTALLED_WIDGET_APPS)

    page = models.ForeignKey("PageInfo")

    game = models.ForeignKey("GameInfo",
        blank=True, null=True,
        help_text="The name of the game in the page.")

    widget = models.CharField(
        blank=True, null=True,
        help_text="The name of the widget in the page.",
        choices=WIDGET_CHOICES,
        max_length=50,)

    enabled = models.BooleanField(
        default=True,
        help_text="Enable ?",)

    class Meta:
        """meta"""
        unique_together = (("page", "game", "widget", ), )
        ordering = ['page', "game", 'widget', ]

    def __unicode__(self):
        return ""


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
        help_text="The priority (ordering) of the game.")

    class Meta:
        """meta"""
        ordering = ['priority', ]

    def __unicode__(self):
        return self.name


class GameSetting(models.Model):
    """Defines the widgets in a game."""
    WIDGET_CHOICES = ((key, key) for key in settings.INSTALLED_WIDGET_APPS)

    game = models.ForeignKey("GameInfo")

    widget = models.CharField(
        help_text="The name of the widget in the page.",
        choices=WIDGET_CHOICES,
        max_length=50,)

    enabled = models.BooleanField(
        default=True,
        help_text="Enable ?",)

    class Meta:
        """meta"""
        unique_together = (("game", "widget", ), )
        ordering = ['game', 'widget', ]

    def __unicode__(self):
        return ""
