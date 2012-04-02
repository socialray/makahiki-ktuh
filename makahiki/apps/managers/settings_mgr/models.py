"""Defines the model containing game settings."""
import datetime
from django.conf import settings
from django.db import models


class ChallengeSettings(models.Model):
    """Defines the global settings for the challenge."""
    site_name = models.CharField(
        default="University of Hawaii at Manoa",
        help_text="The name of the site.",
        max_length=50,)

    competition_name = models.CharField(
        default="Kukui Cup",
        help_text="The name of the competition.",
        max_length=50,)

    competition_point_label = models.CharField(
        default="point",
        help_text="The display label for point.",
        max_length=50,)

    competition_team_label = models.CharField(
        default="Lounge",
        help_text="The display label for team.",
        max_length=50,)

    cas_server_url = models.CharField(
        default="https://login.its.hawaii.edu/cas/",
        help_text="The URL for CAS authentication service.",
        max_length=100,)

    contact_email = models.CharField(
        help_text="The contact email of the admin.",
        max_length=100,)

    # Choices can be found here:
    # http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
    time_zone = models.CharField(
        default="Pacific/Honolulu",
        help_text="The local time zone for this installation.",
        max_length=50,)

    # All choices can be found here:
    # http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
    language_code = models.CharField(
        default="en",
        help_text="The language code for this installation.",
        max_length=50,)

    locale_setting = models.CharField(
        default="en_US.UTF-8",
        help_text="The locale setting for currency conversion.",
        max_length=50,)

    theme = models.CharField(
        default="default",
        help_text="The UI theme for this installation.",
        max_length=50,)

    facebook_app_id = models.CharField(
        default="",
        help_text="The FACEBOOK_APP_ID for facebook integration.",
        max_length=100,)

    facebook_secret_key = models.CharField(
        default="",
        help_text="The FACEBOOK_SECRET_KEY for facebook integration.",
        max_length=100,)

    email_enabled = models.BooleanField(
        default=False,
        help_text="Enable email?",
        )

    email_host = models.CharField(
        default="",
        help_text="The host name of the email server.",
        max_length=100,)

    email_port = models.IntegerField(
        default=587,
        help_text="The port of the email server",)

    email_host_user = models.CharField(
        default="",
        help_text="The username for the email server.",
        max_length=100,)

    email_host_password = models.CharField(
        default="",
        help_text="The user password for the email server.",
        max_length=100,)

    email_use_tls = models.BooleanField(
        default=True,
        help_text="Use TLS in the email server?",)

    def __unicode__(self):
        return self.site_name


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

    @staticmethod
    def set_round_settings():
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

    def save(self, *args, **kwargs):
        """Custom save method."""
        super(RoundSettings, self).save(*args, **kwargs)
        RoundSettings.set_round_settings()


def _get_widget_choice():
    """Retrieves the available page names."""
    return ((key, key) for key in settings.INSTALLED_WIDGET_APPS)


class PageSettings(models.Model):
    """Defines the page settings."""

    PAGE_CHOICES = (("home", "home"),
                    ("help", "help"),
                    ("learn", "learn"),
                    ("win", "win"),
                    ("energy", "energy"),
                    ("advanced", "advanced"),
                    ("profile", "profile"),
                    ("news", "news"),)

    name = models.CharField(
        default="home",
        help_text="The name of the page.",
        choices=PAGE_CHOICES,
        max_length=50,)

    widget = models.CharField(
        default="home",
        help_text="The name of the widget in the page.",
        choices=_get_widget_choice(),
        max_length=50,)

    enabled = models.BooleanField(
        default=True,
        help_text="Enable ?",)

    class Meta:
        """meta"""
        unique_together = (("name", "widget",),)
        ordering = ['name']

    def __unicode__(self):
        return self.name + " : " + self.widget
