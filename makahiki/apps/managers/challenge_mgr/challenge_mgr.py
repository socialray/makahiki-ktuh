"""The manager for challenge related settings."""

import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from apps.managers.challenge_mgr.models import ChallengeSettings, RoundSettings, PageSettings, \
    PageInfo
from apps.utils import utils
from django.core import management


def init():
    """Initialize the challenge."""

    #if settings.DEBUG:
    #    import logging
    #    logger = logging.getLogger('django.db.backends')
    #    logger.setLevel(logging.DEBUG)
    #    logger.addHandler(logging.StreamHandler())

    #    logger = logging.getLogger('django_auth_ldap')
    #    logger.addHandler(logging.StreamHandler())
    #    logger.setLevel(logging.DEBUG)

    if settings.CHALLENGE.competition_name is not None:
        return

    # set the CHALLENGE setting from DB
    ChallengeSettings.set_settings()

    # get the Round settings from DB
    RoundSettings.set_settings()

    # create the admin
    create_admin_user()


def create_admin_user():
    """Create the admin user.
    Creates the admin user if it does not exist. Otherwise, reset the password to the ENV."""
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
    """Returns the challenge name and site."""
    init()
    return "Challenge name : %s @ %s" % (settings.CHALLENGE.competition_name,
                                            settings.CHALLENGE.site_name)


def rounds_info():
    """Returns round info for this challenge."""
    init()

    info_str = ""
    for r in settings.COMPETITION_ROUNDS.keys():
        info_str += r + " ["
        info_str += "start: %s" % settings.COMPETITION_ROUNDS[r]["start"].date().isoformat()
        info_str += ", end: %s" % settings.COMPETITION_ROUNDS[r]["end"].date().isoformat()
        info_str += "]"
    return info_str


def pages():
    """Returns a list of page names in this challenge."""
    return PageInfo.objects.all().values_list("name", flat=True)


def eval_page_unlock(user, page):
    """Returns True if the given page is unlocked based upon evaluation of its dependencies."""
    predicates = page.unlock_condition
    if not predicates:
        return False

    return utils.eval_predicates(predicates, user)


def all_page_info(user):
    """Returns a list of all pages with their current lock state."""
    all_pages = PageInfo.objects.all().order_by("priority")
    for page in all_pages:
        page.is_unlock = eval_page_unlock(user, page)
    return all_pages


def page_info(user, page_name):
    """Returns the specific page info object with its current lock state."""
    page = PageInfo.objects.filter(name=page_name)
    if page:
        page = page[0]
        page.is_unlock = eval_page_unlock(user, page)
        return page
    else:
        return None


def page_settings(page_name):
    """Returns the page settings for the specified page."""
    return PageSettings.objects.filter(page__name=page_name, enabled=True)


def register_page_widget(page_name, widget, label=None):
    """Register the page and widget."""
    if not label:
        label = page_name
    page, _ = PageInfo.objects.get_or_create(name=page_name, label=label)
    PageSettings.objects.get_or_create(page=page, widget=widget)


def available_widgets():
    """Returns a list of all the available widgets for the challenge."""
    return settings.INSTALLED_WIDGET_APPS


def enabled_widgets():
    """Returns a list of all the enabled widgets in the challenge."""
    info_str = ""
    for p in PageSettings.objects.filter(enabled=True):
        info_str += p.name + " : " + p.widget + "\n"
    return info_str


def get_round_info(round_name=None):
    """Returns a dictionary containing round information."""
    rounds = settings.COMPETITION_ROUNDS
    if not round_name:
        return rounds
    elif round_name in rounds:
        return rounds[round_name]
    else:
        return None


def get_current_round_info():
    """Returns the current round and associated dates, or None if not in a round."""
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
    """Return the current round name, or None if not in a round."""
    round_info = get_current_round_info()
    if round_info:
        return round_info["name"]
    else:
        return None


def get_round(submission_date):
    """Return the round associated with the specified date, or else "Overall"."""
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
    """Return True if we are currently in the competition."""
    today = datetime.datetime.today()
    return settings.COMPETITION_START < today and today < settings.COMPETITION_END


class MakahikiBaseCommand(management.base.BaseCommand):
    """The base class for Makahiki command. Used when the init method of the
    challenge_mgr is called."""
    def __init__(self, *args, **kwargs):
        """Initialize the challenge_mgr."""
        init()
        super(MakahikiBaseCommand, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        """Handle the command. Should be overridden by sub class."""
        pass
