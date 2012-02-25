"""
Makahiki specific CAS backend, as an additional AUTHENTICATION_BACKENDS.
"""
from django.core.exceptions import ObjectDoesNotExist
from lib.django_cas.backends import CASBackend, _verify
from django.contrib.auth.models import User


class MakahikiCASBackend(CASBackend):
    """Checks if the login name is a admin or a participant in the cup."""

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
