"""Makahiki specific CAS backends, as an additional AUTHENTICATION_BACKENDS."""

from apps.lib.django_cas.backends import CASBackend, _verify
from apps.managers.player_mgr.player_mgr import get_active_player


class MakahikiCASBackend(CASBackend):
    """Auth Backend to support CAS in Makahiki"""

    def authenticate(self, ticket, service):
        """Verifies CAS ticket and gets or creates User object"""

        username = _verify(ticket, service)
        if not username:
            return None
        else:
            return get_active_player(username)
