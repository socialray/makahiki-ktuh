"""Defines DB models for makahiki settings.
"""
import datetime
from django.db import models


class ChallengeSettings(models.Model):
    """Defines the global settings for the challenge.
    """
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

    setup_wizard_activity_name = models.CharField(
        default="Intro video",
        help_text="The name of the activity in the setup wizard. If the user " \
                  "answers that question correctly, this activity will be " \
                  "marked as completed.",
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

    def __unicode__(self):
        return self.site_name


class RoundSettings(models.Model):
    """Defines the round settings for this challenge.

    Start means the competition will start at midnight on that date.
    End means the competition will end at midnight of that date.
    This means that a round that ends on "2010-08-02" will end at 11:59pm of
    August 1st.
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


class PageSettings(models.Model):
    """Defines the page settings."""

    name = models.CharField(
        default="home",
        help_text="The name of the page.",
        max_length=50,)

    widget = models.CharField(
        default="home",
        help_text="The name of the widget in the page.",
        max_length=50,)

    def __unicode__(self):
        return self.name + " : " + self.widget
