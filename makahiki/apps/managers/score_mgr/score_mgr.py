"""The manager for defining and managing scores."""

from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Sum, Max
from apps.managers.score_mgr.models import ScoreboardEntry, PointsTransaction
from apps.managers.cache_mgr import cache_mgr


def user_round_overall_rank(profile, round_name="Overall"):
    """user round overall rank"""
    entry, _ = ScoreboardEntry.objects.get_or_create(
        profile=profile,
        round_name=round_name
    )

    # Check if the user has done anything.
    if entry.last_awarded_submission:
        return ScoreboardEntry.objects.filter(
            Q(points__gt=entry.points) |
            Q(points=entry.points,
              last_awarded_submission__gt=entry.last_awarded_submission),
            round_name=round_name,
            ).count() + 1

    # Users who have not done anything yet are assumed to be last.
    return ScoreboardEntry.objects.filter(
        points__gt=entry.points,
        round_name=round_name,
        ).count() + 1


def user_round_team_rank(profile, round_name="Overall"):
    """user round team rank"""
    team = profile.team
    entry, _ = ScoreboardEntry.objects.get_or_create(
        profile=profile,
        round_name=round_name
    )

    if entry.last_awarded_submission:
        return ScoreboardEntry.objects.filter(
            Q(points__gt=entry.points) |
            Q(points=entry.points,
              last_awarded_submission__gt=entry.last_awarded_submission),
            profile__team=team,
            round_name=round_name,
            ).count() + 1
    else:
        return ScoreboardEntry.objects.filter(
            points__gt=entry.points,
            profile__team=team,
            round_name=round_name,
            ).count() + 1


def profile_points(profile, round_name="Overall"):
    """Returns the amount of points the user has in the round."""
    entry = ScoreboardEntry.objects.filter(profile=profile, round_name=round_name)
    if entry:
        return entry[0].points
    else:
        return 0


def profile_last_awarded_submission(profile):
    """Returns the last awarded submission date for the profile."""
    entry = profile.scoreboardentry_set.filter(round_name="Overall")
    if entry:
        return entry[0].last_awarded_submission
    else:
        return None


def _update_scoreboard_entry_add(profile, round_name, points, submission_date):
    """Update the scoreboard entry for add_points."""
    entry, _ = ScoreboardEntry.objects.get_or_create(profile=profile, round_name=round_name)
    entry.points += points
    if not entry.last_awarded_submission or submission_date > entry.last_awarded_submission:
        entry.last_awarded_submission = submission_date
    entry.save()


def _update_scoreboard_entry_remove(profile, round_name, points, submission_date):
    """Update the scoreboard entry for remove_points."""
    entry = ScoreboardEntry.objects.get(profile=profile, round_name=round_name)
    entry.points -= points
    if entry.last_awarded_submission == submission_date:
        # Need to find the previous update.
        entry.last_awarded_submission = _last_submitted_before(profile.user, submission_date)
    entry.save()


def add_points(profile, points, submission_date, message, related_object=None):
    """Adds points based on the point value of the submitted object."""
    # Create a transaction first.
    transaction = PointsTransaction(
        user=profile.user,
        points=points,
        submission_date=submission_date,
        message=message,
        )
    if related_object:
        transaction.related_object = related_object

    transaction.save()

    # update the scoreboard entry for the current round and overall round
    current_round = _get_round(submission_date)
    _update_scoreboard_entry_add(profile, current_round, points, submission_date)
    if current_round != "Overall":
        _update_scoreboard_entry_add(profile, "Overall", points, submission_date)

    # Invalidate info bar cache.
    cache_mgr.invalidate_info_bar_cache(profile.user)


def remove_points(profile, points, submission_date, message, related_object=None):
    """Removes points from the user.
    If the submission date is the same as the last_awarded_submission
    field, we rollback to a previously completed task.
    """
    # update the scoreboard entry for the current round and overall round
    current_round = _get_round(submission_date)
    _update_scoreboard_entry_remove(profile, current_round, points, submission_date)
    if current_round != "Overall":
        _update_scoreboard_entry_remove(profile, "Overall", points, submission_date)

    # Log the transaction.
    transaction = PointsTransaction(
        user=profile.user,
        points=points * -1,
        submission_date=submission_date,
        message=message,
        )
    if related_object:
        transaction.related_object = related_object
    transaction.save()

    # Invalidate info bar cache.
    cache_mgr.invalidate_info_bar_cache(profile.user)


def _get_round(submission_date):
    """Get the round that the submission date corresponds to.
       :returns None if it doesn't correspond to anything.
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


def _last_submitted_before(user, submission_date):
    """Time of the last task that was completed before the submission date.
       :returns None if there are no other tasks.
    """
    try:
        return PointsTransaction.objects.filter(
            user=user,
            submission_date__lt=submission_date).latest(
            "submission_date").submission_date
    except ObjectDoesNotExist:
        return None


def team_points_leaders(group, num_results=10, round_name="Overall"):
    """Returns the top points leaders for the given group."""
    return group.team_set.filter(
        profile__scoreboardentry__round_name=round_name).annotate(
            points=Sum("profile__scoreboardentry__points"),
            last=Max("profile__scoreboardentry__last_awarded_submission")).order_by(
                "-points", "-last")[:num_results]


def points_leaders_in_team(team, num_results=10, round_name="Overall"):
    """Gets the individual points leaders for the team."""
    return team.profile_set.select_related('scoreboardentry').filter(
        scoreboardentry__round_name=round_name
    ).order_by("-scoreboardentry__points",
               "-scoreboardentry__last_awarded_submission", )[:num_results]


def team_rank(team, round_name="Overall"):
    """Returns the rank of the team across all groups."""
    aggregate = ScoreboardEntry.objects.filter(
        profile__team=team,
        round_name=round_name).aggregate(points=Sum("points"), last=Max("last_awarded_submission"))

    points = aggregate["points"] or 0
    last_awarded_submission = aggregate["last"]
    # Group by teams, filter out other rounds, and annotate.
    annotated_teams = ScoreboardEntry.objects.values("profile__team").filter(
        round_name=round_name).annotate(team_points=Sum("points"),
                                        last_awarded=Max("last_awarded_submission"))

    count = annotated_teams.filter(team_points__gt=points).count()
    # If there was a submission, tack that on to the count.
    if last_awarded_submission:
        count = count + annotated_teams.filter(
            team_points=points,
            last_awarded_submission__gt=last_awarded_submission
        ).count()

    return count + 1


def team_points(team, round_name="Overall"):
    """Returns the total number of points for the team.  Optional parameter for a round."""
    dictionary = ScoreboardEntry.objects.filter(profile__team=team,
                                                round_name=round_name).aggregate(Sum("points"))
    return dictionary["points__sum"] or 0
