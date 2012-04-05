"""Provides utility methods for invalidating various caches."""

from django.core.cache import cache
from django.utils.hashcompat import md5_constructor
from django.utils.http import urlquote


_makahiki_cache_keys = set()

def info():
    """return the information about this cache."""
    return "%s" % type(cache)


def keys():
    """return the keys in this cache."""
    return _makahiki_cache_keys


def delete(key, version=None):
    """proxy the call to django cache.delete."""
    if key in _makahiki_cache_keys:
        _makahiki_cache_keys.remove(key)
    cache.delete(key, version)


def get(key, default=None, version=None):
    """proxy the call to django cache.get."""
    value = cache.get(key, default, version)
    if value is not None:
        _makahiki_cache_keys.add(key)
    return value


def set(key, value, timeout=None, version=None):
    """proxy the call to django cache.set."""
    _makahiki_cache_keys.add(key)
    cache.set(key, value, timeout, version)


def clear():
    """proxy the call to django cache.clear."""
    _makahiki_cache_keys.clear()
    cache.clear()


def invalidate_template_cache(fragment_name, *variables):
    """Invalidates the cache associated with a template.
    Credit: `djangosnippets.org/snippets/1593/ <http://djangosnippets.org/snippets/1593/>`_"""

    args = md5_constructor(u':'.join([urlquote(var) for var in variables]))
    cache_key = 'template.cache.%s.%s' % (fragment_name, args.hexdigest())
    delete(cache_key)


def invalidate_info_bar_cache(user):
    """Invalidates the user and team caches of the info bar."""
    invalidate_template_cache("infobar", user.username)
    team = user.get_profile().team
    if team:
        invalidate_template_cache("infobar", team.name)


def invalidate_team_avatar_cache(task, user):
    """Invalidates task completed avatar list cache."""
    if task and user and user.get_profile() and user.get_profile().team:
        invalidate_template_cache("team_avatar", task.id, user.get_profile().team.id)


def invalidate_commitments_cache(user):
    """Invalidates the cache of the commitments list for the user."""
    invalidate_template_cache("commitments", user.username)
