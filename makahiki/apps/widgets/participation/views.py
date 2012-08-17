"""Prepares the views for participation widget."""
from apps.managers.cache_mgr import cache_mgr
from apps.managers.team_mgr.models import Team
from apps.widgets.participation.models import TeamParticipation, ParticipationSetting


def supply(request, page_name):
    """Supply the view_objects content for this widget, which is participation data."""

    _ = request
    _ = page_name

    return get_participations()


def get_participations():
    """returns the team participation in categories."""
    return_dict = cache_mgr.get_cache("team_participation")
    if return_dict is None:
        p_settings, _ = ParticipationSetting.objects.get_or_create(pk=1)
        return_dict = {
            "participation_100": [],
            "participation_75": [],
            "participation_50": [],
            "participation_0": [],
            "p_settings": p_settings}
        team_participation = TeamParticipation.objects.all()

        if not team_participation:
            team_participation = Team.objects.all()
            for p in team_participation:
                p.team = p
                p.participation = 0
                return_dict["participation_0"].append(p)
        else:
            for p in team_participation:
                if p.participation >= 100:
                    return_dict["participation_100"].append(p)
                elif p.participation >= 75:
                    return_dict["participation_75"].append(p)
                elif p.participation >= 50:
                    return_dict["participation_50"].append(p)
                else:
                    return_dict["participation_0"].append(p)  # less than 50
        cache_mgr.set_cache("team_participation", return_dict, 3600)
    return return_dict


def remote_supply(request, page_name):
    """Supplies data to remote views."""
    return supply(request, page_name)
