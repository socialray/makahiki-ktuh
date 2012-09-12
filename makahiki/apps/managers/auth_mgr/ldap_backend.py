"""Makahiki specific LDAP backends, as an additional AUTHENTICATION_BACKENDS."""
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django_auth_ldap.backend import LDAPBackend
from apps.managers.player_mgr.player_mgr import get_active_player
from django.contrib.auth.models import User


class MakahikiLDAPBackend(LDAPBackend):
    """Auth Backend to support LDAP in Makahiki"""

    def authenticate(self, username, password):
        """authenticate with LDAP server."""

        if hasattr(settings, "AUTH_LDAP_SERVER_URI"):
            user = super(MakahikiLDAPBackend, self).authenticate(username, password)
            if not user:
                return None
            else:
                return get_active_player(user.username)
        else:
            return None

    def get_or_create_user(self, username, ldap_user):
        """
        This must return a (User, created) 2-tuple for the given LDAP user.
        username is the Django-friendly username of the user. ldap_user.dn is
        the user's DN and ldap_user.attrs contains all of their LDAP attributes.
        """
        try:
            user = User.objects.get(username__iexact=username)
        except ObjectDoesNotExist:
            user = User(username)

        return user, False
