"""The manager for managing team."""
import datetime
from django.db.models.aggregates import Count
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.score_mgr import score_mgr
from apps.managers.team_mgr.models import Team


def team_members(team):
    """Get the team members."""
    return team.profile_set.all()


def team_points_leader(round_name=None):
    """Returns the team points leader (the first place) across all groups, as a Team object."""
    if not round_name:
        round_name = challenge_mgr.get_round_name()

    team_id = score_mgr.team_points_leader(round_name=round_name)
    if team_id:
        return Team.objects.get(id=team_id)
    else:
        teams = Team.objects.all()
        if teams:
            return teams[0]
        else:
            return None


def team_points_leaders(num_results=None, round_name=None):
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


def team_active_participation(num_results=None, round_name=None):
    """Calculate active participation."""
    if not round_name:
        round_name = challenge_mgr.get_round_name()

    active_participation = Team.objects.filter(
        profile__scoreboardentry__points__gte=score_mgr.active_threshold_points(),
        profile__scoreboardentry__round_name=round_name).annotate(
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


def award_member_points(team, points, reason):
    """Award points to the members of the team."""
    count = 0
    for profile in team.profile_set.all():
        if profile.setup_complete:
            today = datetime.datetime.today()
            # Hack to get around executing this script at midnight.  We want to award
            # points earlier to ensure they are within the round they were completed.
            if today.hour == 0:
                today = today - datetime.timedelta(hours=1)

            date = "%d/%d/%d" % (today.month, today.day, today.year)
            profile.add_points(points, today, "%s for %s" % (reason, date))
            profile.save()
            count += 1
    print '%d users in %s are awarded %s points for %s.' % (
        count,
        team,
        points,
        reason)
