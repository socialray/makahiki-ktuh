"""The manager for managing players."""

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from apps.managers.player_mgr.models import Profile
from apps.managers.score_mgr import score_mgr
from apps.managers.team_mgr.models import Team
from apps.widgets.badges.models import BadgeAward


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


def points_leader(round_name=None):
    """Returns the points leader (the first place) out of all users, as a Profile object."""
    entry = score_mgr.player_points_leader(round_name=round_name)
    if entry:
        return entry
    else:
        return Profile.objects.all()[0]


def points_leaders(num_results=None, round_name=None):
    """Returns the points leaders out of all users, as a dictionary object
    with profile__name and points.
    """
    entries = score_mgr.player_points_leaders(num_results=num_results, round_name=round_name)
    if entries:
        for e in entries:
            u = Profile.objects.get(pk=e['profile']).user
            p = u.get_profile()
            e['badges'] = BadgeAward.objects.filter(profile=p)
        return entries
    else:
        results = Profile.objects.all().extra(select={'profile__name': 'name', 'points': 0}).values(
            'profile__name', 'points')
        if num_results:
            results = results[:num_results]
        return results


def create_player(username, password, email, firstname, lastname, team_name, is_ra):
    """Create a player with the assigned team"""
    try:
        user = User.objects.get(username=username)
        user.delete()
        print "Existing user '%s' deleted." % username
    except ObjectDoesNotExist:
        pass

    user = User.objects.create_user(username, email, password)
    user.first_name = firstname
    user.last_name = lastname
    user.save()

    profile = user.get_profile()
    profile.name = firstname + " " + lastname[:1] + "."
    profile.is_ra = is_ra

    try:
        profile.team = Team.objects.get(name=team_name)
    except ObjectDoesNotExist:
        print "Can not find team '%s', set the team of the player '%s' to None." % \
              (team_name, profile.name)

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
    profile.team = team

    profile.save()


def get_user_by_email(email):
    """Return the user from given email"""
    try:
        return User.objects.get(email=email)
    except ObjectDoesNotExist:
        return None
