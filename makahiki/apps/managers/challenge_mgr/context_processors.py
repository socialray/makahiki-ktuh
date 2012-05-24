"""Provides competition settings in the request context to be used within a template."""
from django.utils import importlib
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.player_mgr.models import Profile
from apps.managers.team_mgr.models import Team
from apps.widgets.smartgrid import smartgrid
from django.conf import settings


def competition(request):
    """Provides access to standard competition constants within a template.

    :param request: The request object.
    :return: a dictionary of game settings."""
    # Get user-specific information.

    user = request.user
    team_member_count = None
    team_count = None
    overall_member_count = None
    available_events = None
    default_view_objects = None
    page_info = None
    css_theme = settings.CHALLENGE.theme

    if user.is_authenticated():
        profile = user.get_profile()

        default_view_objects = _get_default_view_objects(request)
        page_info = challenge_mgr.page_info(user)

        if profile.team:
            team_member_count = user.get_profile().team.profile_set.count()
            team_count = Team.objects.count()
            overall_member_count = Profile.objects.count()
            available_events = smartgrid.get_available_events(user)

        # override the site theme if there is any
        if profile.theme:
            css_theme = profile.theme

    return {
        "CHALLENGE": settings.CHALLENGE,
        "CSS_THEME": css_theme,
        "TEAM_LABEL": settings.CHALLENGE.competition_team_label,
        "FACEBOOK_APP_ID": settings.FACEBOOK_APP_ID,
        "MAKAHIKI_USE_LESS": settings.MAKAHIKI_USE_LESS,
        "CURRENT_ROUND_INFO": challenge_mgr.get_current_round_info(),
        "IN_COMPETITION": challenge_mgr.in_competition(),
        "TEAM_COUNT": team_count,
        "TEAM_MEMBER_COUNT": team_member_count,
        "OVERALL_MEMBER_COUNT": overall_member_count,
        "DEFAULT_VIEW_OBJECTS": default_view_objects,
        "AVAILABLE_EVENTS": available_events,
        "PAGE_INFO": page_info,
    }


def _get_default_view_objects(request):
    """Load the default widgets view objects for all pages."""

    default_view_objects = {}
    for widget in settings.INSTALLED_DEFAULT_WIDGET_APPS:
        view_module_name = 'apps.widgets.' + widget + '.views'
        page_views = importlib.import_module(view_module_name)
        widget = widget.replace(".", "_")
        default_view_objects[widget] = page_views.supply(request, None)
    return default_view_objects
