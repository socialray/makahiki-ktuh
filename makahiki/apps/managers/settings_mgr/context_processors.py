"""
 provides competition settings in the request context to be used within
 a template. It mainly retrieve the settings from settings files.
"""
from django.conf import settings
from managers.settings_mgr import get_rounds_for_header, \
        get_current_round, get_current_round_info, in_competition
from managers.player_mgr.models import Profile
from managers.team_mgr.models import Team

def competition(request):
    """Provides access to standard competition constants within a template."""
    # Get user-specific information.
    user = request.user
    team_member_count = None
    if user.is_authenticated() and user.get_profile().team:
        team_member_count = user.get_profile().team.profile_set.count()

    team_count = Team.objects.count()
    overall_member_count = Profile.objects.count()

    # Get current round info.
    current_round = get_current_round() or "Overall"

    # Get Facebook info.
    try:
        facebook_app_id = settings.FACEBOOK_APP_ID
    except AttributeError:
        facebook_app_id = None

    return {
        "STATIC_URL": settings.STATIC_URL,
        "SITE_NAME": settings.SITE_NAME,
        "COMPETITION_NAME": settings.COMPETITION_NAME,
        "COMPETITION_POINT_LABEL": settings.COMPETITION_POINT_LABEL or "point",
        "CSS_THEME": settings.MAKAHIKI_THEME,
        "THEME_NAME": settings.MAKAHIKI_THEME,
        "TEAM_COUNT": team_count,
        "TEAM_MEMBER_COUNT": team_member_count,
        "OVERALL_MEMBER_COUNT": overall_member_count,
        "ROUNDS": get_rounds_for_header(),
        "TEAM_LABEL": settings.COMPETITION_TEAM_LABEL or "Team",
        "CURRENT_ROUND": current_round,
        "CURRENT_ROUND_INFO": get_current_round_info(),
        "FACEBOOK_APP_ID": facebook_app_id,
        "IN_COMPETITION": in_competition(),
    }

