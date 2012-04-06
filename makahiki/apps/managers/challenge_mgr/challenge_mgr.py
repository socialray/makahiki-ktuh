"""The manager for challenge related settings."""

import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from apps.managers.challenge_mgr.models import ChallengeSettings, RoundSettings, PageSettings


def load_settings():
    """Load settings for this challenge."""

    # get the CALLENGE setting from DB
    set_challenge_settings()

    # get the Round settings from DB
    RoundSettings.set_round_settings()

    # register the home page and widget
    PageSettings.objects.get_or_create(name="home", widget="home")


def set_challenge_settings():
    """get the CALLENGE setting from DB."""
    settings.CHALLENGE, _ = ChallengeSettings.objects.get_or_create(pk=1)

    # required setting for the CAS authentication service.
    settings.CAS_SERVER_URL = settings.CHALLENGE.cas_server_url

    # global settings
    settings.LOCALE_SETTING = settings.CHALLENGE.locale_setting
    settings.TIME_ZONE = settings.CHALLENGE.time_zone
    settings.LANGUAGE_CODE = settings.CHALLENGE.language_code

    # email settings
    if settings.CHALLENGE.email_enabled:
        settings.EMAIL_HOST = settings.CHALLENGE.email_host
        settings.EMAIL_PORT = settings.CHALLENGE.email_port
        settings.EMAIL_HOST_USER = settings.CHALLENGE.email_host_user
        settings.EMAIL_HOST_PASSWORD = settings.CHALLENGE.email_host_password
        settings.EMAIL_USE_TLS = settings.CHALLENGE.email_use_tls


def create_admin_user():
    """Create admin user.

    Create the admin user if not exists. otherwise, reset the password to the ENV.
    """
    try:
        user = User.objects.get(username=settings.ADMIN_USER)
        if not user.check_password(settings.ADMIN_PASSWORD):
            user.set_password(settings.ADMIN_PASSWORD)
            user.save()
    except ObjectDoesNotExist:
        user = User.objects.create_superuser(settings.ADMIN_USER, "", settings.ADMIN_PASSWORD)
        profile = user.get_profile()
        profile.setup_complete = True
        profile.setup_profile = True
        profile.completion_date = datetime.datetime.today()
        profile.save()


def info():
    """returns the information about the challenge."""
    if settings.CHALLENGE.competition_name is None:
        load_settings()

    return "Challenge name : %s \n" \
           "Rounds: %s" % (settings.CHALLENGE.competition_name,
                           settings.COMPETITION_ROUNDS)


def get_round_info():
    """Returns a dictionary containing round information."""
    rounds = settings.COMPETITION_ROUNDS
    return rounds


def get_current_round():
    """Get the current round name."""
    round_info = get_current_round_info()
    if round_info is not None:
        return round_info["name"]
    else:
        return None


def get_current_round_info():
    """Gets the current round and associated dates."""
    rounds = get_round_info()
    today = datetime.datetime.today()
    for key in rounds.keys():
        start = rounds[key]["start"]
        end = rounds[key]["end"]
        if today >= start and today < end:
            return {
                "name": key,
                "start": start,
                "end": end,
                }

    # No current round.
    return None


def in_competition():
    """Returns true if we are still in the competition."""
    today = datetime.datetime.today()
    return settings.COMPETITION_START < today and today < settings.COMPETITION_END
