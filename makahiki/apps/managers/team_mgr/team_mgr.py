"""The manager for managing team."""
from django.db.models.aggregates import Count
from apps.managers.score_mgr import score_mgr
from apps.managers.team_mgr.models import Team


def team_members(team):
    """Get the team members."""
    return team.profile_set.all()


def team_points_leader(round_name="Overall"):
    """Returns the team points leader (the first place) across all groups, as a Team object."""
    team_id = score_mgr.team_points_leader(round_name=round_name)
    if team_id:
        return Team.objects.get(id=team_id)
    else:
        return Team.objects.all()[0]


def team_points_leaders(num_results=None, round_name="Overall"):
    """Returns the team points leaders across all groups, as a dictionary profile__team__name
    and points.
    """
    entry = score_mgr.team_points_leaders(num_results=num_results, round_name=round_name)
    if entry:
        return entry
    else:
        results = Team.objects.all().extra(
            select={'profile__team__name': 'name', 'points': 0}).values(
            'profile__team__name', 'points')
        if num_results:
            results = results[:num_results]
        return results


def team_active_participation(num_results=None):
    """Calculate active participation."""
    active_participation = Team.objects.filter(
        profile__scoreboardentry__points__gte=score_mgr.active_threshold_points(),
        profile__scoreboardentry__round_name="Overall").annotate(
            user_count=Count('profile')).order_by('-user_count').select_related(
                'group')

    if num_results:
        active_participation = active_participation[:num_results]

    participation = []
    for t in active_participation:
        t.active_participation = (t.user_count * 100) / t.profile_set.count()
        participation.append(t)

    for t in Team.objects.all():
        if len(participation) == num_results:
            break

        if not t in active_participation:
            t.active_participation = 0
            participation.append(t)

    return participation
