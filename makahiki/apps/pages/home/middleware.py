"""
home page middleware to check if setup completed and restricted page re-direction.
"""
import re
import datetime

from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class CheckSetupMiddleware(object):
    """This middleware checks if the logged in user has completed the setup process."""

    def process_request(self, request):
        """ check to see if setup completed."""
        user = request.user
        path = request.path
        # We need to check if the user is going to the home page so we don't get caught
        # in a redirect loop.
        # We do need to filter out requests for CSS and other resources.
        pattern = re.compile(
            "^/(m\/admin|m\/setup|admin|log|account|home|site_media|tc|media|favicon.ico)/")
        needs_setup = user.is_authenticated() and not user.get_profile().setup_complete
        if needs_setup and not pattern.match(path):
            return HttpResponseRedirect("/")
        return None


class CompetitionMiddleware(object):
    """
    This middleware checks if the competition is over.
    """

    def process_request(self, request):
        """
        Checks if we are still in the competition. If the user is logged in,
        they are redirected to a competition status page.
        """
        if request.user.is_authenticated():
            path = request.path

            today = datetime.datetime.today()
            start = datetime.datetime.strptime(settings.COMPETITION_START, "%Y-%m-%d")
            end = datetime.datetime.strptime(settings.COMPETITION_END, "%Y-%m-%d")

            staff_user = request.user.is_staff or request.session.get('staff', False)

            pattern = re.compile("^/(m\/|home\/restricted|site_media|media|favicon.ico)/")

            if today < start and not staff_user and not pattern.match(path):
                return HttpResponseRedirect(reverse("home_restricted"))

            if today > end and not staff_user and not pattern.match(path):
                return HttpResponseRedirect(reverse("home_restricted"))

        return None
