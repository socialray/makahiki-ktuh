"""Makahiki specific backends, as an additional AUTHENTICATION_BACKENDS."""

from django.core.exceptions import ObjectDoesNotExist
from apps.lib.django_cas.backends import CASBackend, _verify
from django.contrib.auth.models import User
from django_auth_ldap.backend import LDAPBackend


class MakahikiCASBackend(CASBackend):
    """Auth Backend to support CAS in Makahiki"""

    def authenticate(self, ticket, service):
        """Verifies CAS ticket and gets or creates User object"""

        username = _verify(ticket, service)
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
            return user if user.is_active else None
        except ObjectDoesNotExist:
            return None


class MakahikiLDAPBackend(LDAPBackend):
    """Auth Backend to support LDAP in Makahiki"""

    def authenticate(self, username, password):
        """authenticate with LDAP server."""

        username = super(MakahikiLDAPBackend, self).authenticate(username, password)
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
            return user if user.is_active else None
        except ObjectDoesNotExist:
            return None
