"""The manager for managing players."""

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query_utils import Q
from django.db.utils import IntegrityError
from apps.managers.player_mgr.models import Profile
from apps.managers.score_mgr import score_mgr
from apps.managers.team_mgr.models import Team


def get_active_player(username):
    """return User object if the player is active, otherwise, return None"""
    try:
        username = username.lower()
        user = User.objects.get(username=username)
        return user if user.is_active else None
    except ObjectDoesNotExist:
        return None


def players(num_results=None):
    """Get some numbers of players."""

    results = Profile.objects.all()
    if num_results:
        results = results[:num_results]
    return results


def canopy_members():
    """returns the canopy memebers, which are the top 50 points leaders, plus admin."""

    members = []
    entries = score_mgr.player_points_leaders(num_results=50)
    if entries:
        for entry in entries:
            member = User.objects.get(profile__id=entry["profile"])
            members.append(member)

    entries = User.objects.filter(Q(is_superuser=True) |
                                  Q(is_staff=True)).select_related('profile')
    for entry in entries:
        members.append(entry)

    return members


def points_leader(round_name="Overall"):
    """Returns the points leader (the first place) out of all users, as a Profile object."""
    entry = score_mgr.player_points_leader(round_name=round_name)
    if entry:
        return entry
    else:
        return Profile.objects.all()[0]


def points_leaders(num_results=None, round_name="Overall"):
    """Returns the points leaders out of all users, as a dictionary object
    with profile__name and points.
    """
    entries = score_mgr. player_points_leaders(num_results=num_results, round_name=round_name)
    if entries:
        return entries
    else:
        results = Profile.objects.all().extra(select={'profile__name': 'name', 'points': 0}).values(
            'profile__name', 'points')
        if num_results:
            results = results[:num_results]
        return results


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


def get_user_by_email(email):
    """Return the user from given email"""
    try:
        return User.objects.get(email=email)
    except ObjectDoesNotExist:
        return None
