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
    """initialize the challenge."""

    if settings.CHALLENGE.competition_name is not None:
        return

    # set the CHALLENGE setting from DB
    ChallengeSettings.set_settings()

    # get the Round settings from DB
    RoundSettings.set_settings()

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


def pages():
    """returns all the page name in the challenge."""
    return PageInfo.objects.all().values_list("name", flat=True)


def has_points(user, points):
    """returns True if the user has more than the specific points."""
    return user.get_profile().points() >= points


PAGE_PREDICATES = {
    "has_points": has_points,
}


def eval_page_unlock(user, page):
    """Determine the unlock status of a task by dependency expression"""
    predicates = page.unlock_condition
    if not predicates:
        return False

    return utils.eval_predicates(predicates, user, PAGE_PREDICATES)


def page_info(user):
    """returns the page settings."""
    all_pages = PageInfo.objects.all().order_by("priority")
    for page in all_pages:
        page.is_unlock = eval_page_unlock(user, page)
    return all_pages


def page_settings(page_name):
    """return the page widget settings of the page."""
    return PageSettings.objects.filter(page__name=page_name, enabled=True)


def register_page_widget(page_name, widget, label=None):
    """ register the page and widget."""
    if not label:
        label = page_name
    page, _ = PageInfo.objects.get_or_create(name=page_name, label=label)
    PageSettings.objects.get_or_create(page=page, widget=widget)


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


class MakahikiBaseCommand(management.base.BaseCommand):
    """The base class for Makahiki command. It is to be used when the init method of the
    challenge_mgr need to be called."""
    def __init__(self, *args, **kwargs):
        """initiailze the challenge_mgr."""
        init()
        super(MakahikiBaseCommand, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        """handle the command. should be override by sub class."""
        pass