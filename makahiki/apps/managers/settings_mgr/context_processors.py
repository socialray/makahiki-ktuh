"""Provides competition settings in the request context to be used within a template."""
from apps.managers.settings_mgr import get_current_round_info, in_competition
from apps.managers.player_mgr.models import Profile
from apps.managers.team_mgr.models import Team
import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from apps.managers.settings_mgr.models import ChallengeSettings, RoundSettings, PageSettings


def _load_db_settings():
    """Load additional settings from DB."""

    # get the CALLENGE setting from DB
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

    # get the Round settings from DB
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

    # register the home page and widget
    PageSettings.objects.get_or_create(name="home", widget="home")


def _create_admin_user():
    """Create admin user.

    Create the admin user if not exists. otherwise, reset the password to the ENV.
    """
    print settings.ADMIN_USER
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


def competition(request):
    """Provides access to standard competition constants within a template.

:param request: The request object.
:return: a dictionary of game settings."""
    # Get user-specific information.

    user = request.user
    team_member_count = None
    if user.is_authenticated() and user.get_profile().team:
        team_member_count = user.get_profile().team.profile_set.count()

    team_count = Team.objects.count()
    overall_member_count = Profile.objects.count()

    # load the db settings if not done yet.
    if settings.CHALLENGE.competition_name is None:
        _load_db_settings()
        _create_admin_user()

    # Get Facebook info.
    try:
        facebook_app_id = settings.CHALLENGE.facebook_app_id
    except AttributeError:
        facebook_app_id = None

    return {
        "STATIC_URL": settings.STATIC_URL,
        "SITE_NAME": settings.CHALLENGE.site_name,
        "COMPETITION_NAME": settings.CHALLENGE.competition_name,
        "COMPETITION_POINT_LABEL": settings.CHALLENGE.competition_point_label,
        "CSS_THEME": settings.CHALLENGE.theme,
        "THEME_NAME": settings.CHALLENGE.theme,
        "TEAM_COUNT": team_count,
        "TEAM_MEMBER_COUNT": team_member_count,
        "OVERALL_MEMBER_COUNT": overall_member_count,
        "TEAM_LABEL": settings.CHALLENGE.competition_team_label,
        "CURRENT_ROUND_INFO": get_current_round_info(),
        "FACEBOOK_APP_ID": facebook_app_id,
        "IN_COMPETITION": in_competition(),
    }
