"""The manager for managing players."""

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from apps.managers.player_mgr.models import Profile
from apps.managers.score_mgr import point_score_mgr
from apps.managers.team_mgr.models import Team


def players(num_results=10):
    """Get some numbers of players."""
    return Profile.objects.all()[:num_results]


def points_leader(round_name="Overall"):
    """Returns the points leader (the first place) out of all users, as a Profile object."""
    entry = point_score_mgr.player_points_leader(round_name=round_name)
    if entry:
        return entry
    else:
        return Profile.objects.all()[0]


def points_leaders(num_results=10, round_name="Overall"):
    """Returns the points leaders out of all users, as a dictionary object
    with profile__name and points.
    """
    entry = point_score_mgr.player_points_leaders(num_results=num_results, round_name=round_name)
    if entry:
        return entry
    else:
        return Profile.objects.all().extra(select={'profile__name': 'name', 'points': 0}).values(
            'profile__name', 'points')[:num_results]


def create_player(username, email, firstname, lastname, team_name):
    """Create a player with the assigned team"""
    try:
        user = User.objects.get(username=username)
        user.delete()
    except ObjectDoesNotExist:
        pass

    user = User.objects.create_user(username, email)
    user.first_name = firstname
    user.last_name = lastname
    user.save()

    profile = user.get_profile()
    profile.first_name = firstname
    profile.last_name = lastname
    profile.name = firstname + " " + lastname[:1] + "."
    profile.team = Team.objects.get(name=team_name)
    try:
        profile.save()
    except IntegrityError:
        profile.name = firstname + " " + lastname
        profile.save()


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
