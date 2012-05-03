"""Defines the model containing game settings."""
import datetime
from django.conf import settings
from django.db import models
from apps.utils.utils import media_file_path, OverwriteStorage


class ChallengeSettings(models.Model):
    """Defines the global settings for the challenge."""
    site_name = models.CharField(
        default="University of Hawaii at Manoa",
        help_text="The name of the site.",
        max_length=50,)
    site_domain = models.CharField(
        default="kukuicup.manoa.hawaii.edu",
        help_text="The domain name of the site.",
        max_length=100,)
    site_logo = models.ImageField(
        upload_to=media_file_path(),
        storage=OverwriteStorage(),
        max_length=255, blank=True, null=True,
        help_text="The logo of the site.",)
    competition_name = models.CharField(
        default="Kukui Cup",
        help_text="The name of the competition.",
        max_length=50,)
    theme = models.CharField(
        default="default",
        help_text="The UI theme for this installation.",
        max_length=50,)
    competition_team_label = models.CharField(
        default="Lounge",
        help_text="The display label for team.",
        max_length=50,)
    cas_server_url = models.CharField(
        default="https://login.its.hawaii.edu/cas/",
        help_text="The URL for CAS authentication service.",
        max_length=100,)

    # email settings
    email_enabled = models.BooleanField(
        default=False,
        help_text="Enable email?",
        )
    contact_email = models.CharField(
        help_text="The contact email of the admin.",
        max_length=100,)
    email_host = models.CharField(
        default="",
        help_text="The host name of the email server.",
        max_length=100,)
    email_port = models.IntegerField(
        default=587,
        help_text="The port of the email server",)
    email_use_tls = models.BooleanField(
        default=True,
        help_text="Use TLS in the email server?",)

    # landing page content settings
    landing_slogan = models.TextField(
        default="The Kukui Cup: Lights out, game on!",
        help_text="The slogan text in the landing page. " + settings.MARKDOWN_TEXT,
        max_length=255,)
    landing_introduction = models.TextField(
        default="Aloha!",
        help_text="The introduction in the landing page. " + settings.MARKDOWN_TEXT,
        max_length=500,)
    landing_participant_text = models.TextField(
        default="Let me in",
        max_length=255,
        help_text="The text of the participant button in the landing page. " +
                  settings.MARKDOWN_TEXT)
    landing_non_participant_text = models.TextField(
        default="About",
        max_length=255,
        help_text="The text of the non participant button in the landing page. " +
                  settings.MARKDOWN_TEXT)
    landing_sponsors = models.TextField(
        default="",
        help_text="The sponsors in the landing page. " + settings.MARKDOWN_TEXT,
        max_length=255,)

    def __unicode__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        """Custom save method."""
        super(ChallengeSettings, self).save(*args, **kwargs)
        ChallengeSettings.set_settings()

    @staticmethod
    def set_settings():
        """get the CALLENGE setting from DB and set the global django settings."""
        settings.CHALLENGE, _ = ChallengeSettings.objects.get_or_create(pk=1)

        # required setting for the CAS authentication service.
        settings.CAS_SERVER_URL = settings.CHALLENGE.cas_server_url

        # email settings
        if settings.CHALLENGE.email_enabled:
            settings.SERVER_EMAIL = settings.CHALLENGE.contact_email
            settings.EMAIL_HOST = settings.CHALLENGE.email_host
            settings.EMAIL_PORT = settings.CHALLENGE.email_port
            settings.EMAIL_USE_TLS = settings.CHALLENGE.email_use_tls
            settings.ADMINS = (('Admin', settings.CHALLENGE.contact_email),)


class RoundSettings(models.Model):
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
        super(RoundSettings, self).save(*args, **kwargs)
        RoundSettings.set_settings()

    @staticmethod
    def set_settings():
        """set the round info in the system settings."""
        rounds = RoundSettings.objects.all()
        if rounds.count() == 0:
            RoundSettings.objects.create()
            rounds = RoundSettings.objects.all()

        #store in a round dictionary and calculate start and end
        rounds_dict = {}
        settings.COMPETITION_START = None
        last_round = None
        for competition_round in rounds:
            if settings.COMPETITION_START is None:
                settings.COMPETITION_START = competition_round.start
            rounds_dict[competition_round.name] = {
                "start": competition_round.start,
                "end": competition_round.end, }
            last_round = competition_round
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

    def __unicode__(self):
        return self.name


class PageSettings(models.Model):
    """Defines the page and widget settings."""
    WIDGET_CHOICES = ((key, key) for key in settings.INSTALLED_WIDGET_APPS)

    page = models.ForeignKey("PageInfo")

    widget = models.CharField(
        default="home",
        help_text="The name of the widget in the page.",
        choices=WIDGET_CHOICES,
        max_length=50,)

    enabled = models.BooleanField(
        default=True,
        help_text="Enable ?",)

    class Meta:
        """meta"""
        unique_together = (("page", "widget", ), )
        ordering = ['page', 'widget', ]

    def __unicode__(self):
        return ""
