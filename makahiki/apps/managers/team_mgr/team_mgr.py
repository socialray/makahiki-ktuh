"""The manager for managing team."""
from apps.managers.score_mgr import score_mgr
from apps.managers.team_mgr.models import Team


def team_members(team):
    """Get the team members."""
    return team.profile_set()


def team_points_leader(round_name="Overall"):
    """Returns the team points leader (the first place) across all groups, as a Team object."""
    team_id = score_mgr.team_points_leader(round_name=round_name)
    if team_id:
        return Team.objects.get(id=team_id)
    else:
        return Team.objects.all()[0]


def team_points_leaders(num_results=10, round_name="Overall"):
    """Returns the team points leaders across all groups, as a dictionary profile__team__name
    and points.
    """
    entry = score_mgr.team_points_leaders(num_results=num_results, round_name=round_name)
    if entry:
        return entry
    else:
        return Team.objects.all().extra(select={'profile__team__name': 'name', 'points': 0}).values(
            'profile__team__name', 'points')[:num_results]
