"""The manager for managing players."""

from django.contrib.auth.models import User
from apps.managers.player_mgr.models import Profile


def players(num_results=10):
    """Get some numbers of players."""
    return Profile.objects.all()[:num_results]


def points_leaders(num_results=10, round_name="Overall"):
    """Returns the top points leaders out of all users."""
    entries = Profile.objects.filter(
        scoreboardentry__round_name=round_name,).order_by(
        "-scoreboardentry__points",
        "-scoreboardentry__last_awarded_submission")
    if entries:
        return entries[:num_results]
    else:
        return Profile.objects.all()[:num_results]


def reset_user(user):
    """Resets the given user by deleting them and then restoring them. """
    username = user.username
    email = user.email
    is_staff = user.is_staff
    is_superuser = user.is_superuser

    profile = user.get_profile()
    d_name = profile.name
    f_name = profile.first_name
    l_name = profile.last_name
    team = profile.team

    # Delete the user and create a new one.
    user.delete()
    new_user = User.objects.create_user(username=username, email=email,
                                        password="")
    new_user.is_staff = is_staff
    new_user.is_superuser = is_superuser
    new_user.save()

    profile = new_user.get_profile()
    profile.name = d_name
    profile.first_name = f_name
    profile.last_name = l_name
    profile.team = team

    profile.save()
