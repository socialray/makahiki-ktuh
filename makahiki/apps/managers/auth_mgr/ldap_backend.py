"""Makahiki specific LDAP backends, as an additional AUTHENTICATION_BACKENDS."""
from django.conf import settings
from django_auth_ldap.backend import LDAPBackend
from apps.managers.player_mgr.player_mgr import get_active_player


class MakahikiLDAPBackend(LDAPBackend):
    """Auth Backend to support LDAP in Makahiki"""

    def authenticate(self, username, password):
        """authenticate with LDAP server."""

        if hasattr(settings, "AUTH_LDAP_SERVER_URI"):
            username = super(MakahikiLDAPBackend, self).authenticate(username, password)
            if not username:
                return None
            else:
                return get_active_player(username)
        else:
            return None
