"""The manager for challenge related settings."""

import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from apps.managers.challenge_mgr.models import ChallengeSettings, RoundSettings, PageSettings


def init():
    """initialize the challenge."""

    if settings.CHALLENGE.competition_name is not None:
        return

    # set the CHALLENGE setting from DB
    ChallengeSettings.set_settings()

    # get the Round settings from DB
    RoundSettings.set_settings()

    # register the home page and widget
    PageSettings.objects.get_or_create(name="home", widget="home")

    # create the admin
    create_admin_user()


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
    init()
    return "Challenge name : %s @ %s" % (settings.CHALLENGE.competition_name,
                                            settings.CHALLENGE.site_name)


def rounds_info():
    """returns the round info about the challenge."""
    init()

    info_str = ""
    for r in settings.COMPETITION_ROUNDS.keys():
        info_str += r + " ["
        info_str += "start: %s" % settings.COMPETITION_ROUNDS[r]["start"].date().isoformat()
        info_str += ", end: %s" % settings.COMPETITION_ROUNDS[r]["end"].date().isoformat()
        info_str += "]"
    return info_str


def available_widgets():
    """returns all the available widgets for the challenge."""
    return settings.INSTALLED_WIDGET_APPS


def enabled_widgets():
    """returns all the enabled widgets in the challenge."""
    info_str = ""
    for p in PageSettings.objects.filter(enabled=True):
        info_str += p.name + " : " + p.widget + "\n"
    return info_str


def get_round_info():
    """Returns a dictionary containing round information."""
    rounds = settings.COMPETITION_ROUNDS
    return rounds


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


def get_current_round():
    """Get the current round name."""
    round_info = get_current_round_info()
    if round_info is not None:
        return round_info["name"]
    else:
        return None


def get_round(submission_date):
    """Get the round that the specified date corresponds to.
       :returns Overall if it doesn't correspond to anything.
    """
    rounds = settings.COMPETITION_ROUNDS

    # Find which round this belongs to.
    if rounds is not None:
        for key in rounds:
            start = rounds[key]["start"]
            end = rounds[key]["end"]
            if submission_date >= start and submission_date < end:
                return key

    return "Overall"


def in_competition():
    """Returns true if we are still in the competition."""
    today = datetime.datetime.today()
    return settings.COMPETITION_START < today and today < settings.COMPETITION_END
