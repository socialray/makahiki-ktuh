"""analysis module."""

from django.contrib.auth.models import User
from apps.managers.log_mgr.models import MakahikiLog
from apps.managers.player_mgr.models import Profile
from apps.widgets.smartgrid.models import ActionMember, Action


MIN_SESSION = 60  # Assume user spends 60 seconds on a single page.


def calculate_summary_stats():
    """calculate the summary."""
    output = '=== Summary Stats ===\n'

    output += "%s,%d\n" % (
        "Total number of social submission",
        ActionMember.objects.filter(social_email__isnull=True).count()
    )
    output += "%s,%d\n" % (
        "Total number of referrals",
        Profile.objects.filter(referring_user__isnull=False).count()
    )
    return output


def calculate_user_stats():
    """Calculate the user stats."""
    output = '=== User Stats ===\n'

    users = User.objects.filter(is_superuser=False)
    output += 'user id,total seconds spent,total hours spent,total submissions,total points\n'

    for user in users:
        logs = MakahikiLog.objects.filter(remote_user=user.username).order_by(
            'request_time')
        total_time = _user_time_spent(logs)

        total_submission = _user_submissions(user)

        total_point = _user_points(user)

        output += '%d,%d,%.2f,%d,%d\n' % (
            user.id, total_time, total_time / 3600.0,
            total_submission, total_point)
    return output


def calculate_action_stats():
    """action stats"""
    output = '=== Action Stats ===\n'

    output += 'action_type,total_actions\n'

    actions = Action.objects.filter(level__isnull=False, category__isnull=False)

    output += "%s,%d\n" % (
        "activity", actions.filter(type="activity").count()
    )

    output += "%s,%d\n" % (
        "event", actions.filter(type="event").count()
        )
    output += "%s,%d\n" % (
        "excursion", actions.filter(type="excursion").count()
        )

    output += "%s,%d\n" % (
        "commitment", actions.filter(type="commitment").count()
        )

    return output


def _user_submissions(user):
    """
    user submissions.
    """
    return ActionMember.objects.filter(user=user).count()


def _user_points(user):
    """user points."""
    return user.get_profile().points()


def _user_time_spent(logs, start_date=None):
    """ Iterate over the logs and track previous time and time spent."""
    query = logs
    if start_date:
        query = query.filter(request_time__gt=start_date)

    if query.count() > 0:
        prev = query[0].request_time
        cur_session = total = 0
        for log in query[1:]:
            current = log.request_time
            diff = current - prev
            # Start a new interval if 30 minutes have passed.
            if diff.total_seconds() > (60 * 30):
                if cur_session == 0:
                    total += MIN_SESSION
                else:
                    total += cur_session
                cur_session = 0
            else:
                cur_session += diff.total_seconds()

            prev = current

        # Append any session that was in progress.
        total += cur_session
        return total

    return 0
