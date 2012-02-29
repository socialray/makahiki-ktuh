"""
This middleware class handles login check and tracking for every user login.
"""

import datetime
import re
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from apps.managers.settings_mgr import in_competition


class LoginMiddleware(object):
    """
    This middleware does the following checks and tracking:
    1. check if today is in the competition period
    2. check if user has completed the setup
    3. tracks how many days in a row the user has come to the site.
    """

    def process_request(self, request):
        """process the request"""
        response = self.check_competition_period(request)
        if response is None:
            response = self.check_setup_completed(request)
            if response is None:
                response = self.track_login(request)
        return response

    def track_login(self, request):
        """Checks if the user is logged in and updates the tracking field."""
        user = request.user
        if user.is_authenticated():
            profile = request.user.get_profile()
            last_visit = request.user.get_profile().last_visit_date
            today = datetime.date.today()

            # Look for a previous login.
            if last_visit and (today - last_visit) == datetime.timedelta(
                days=1):
                profile.last_visit_date = today
                profile.daily_visit_count += 1
                profile.save()
            elif not last_visit or (today - last_visit) > datetime.timedelta(
                days=1):
                # Reset the daily login count.
                profile.last_visit_date = today
                profile.daily_visit_count = 1
                profile.save()

        return None

    def check_setup_completed(self, request):
        """ check to see if setup completed."""
        user = request.user
        path = request.path
        # We need to check if the user is going to the home page so we don't
        # get caught in a redirect loop. We do need to filter out requests
        # for CSS and other resources.
        pattern = re.compile("^/"
                             "(m\/admin|m\/setup|admin|log|account|home|"
                             "site_media|tc|media|favicon.ico)/")
        needs_setup = user.is_authenticated() and not user.get_profile()\
        .setup_complete
        if needs_setup and not pattern.match(path):
            return HttpResponseRedirect("/")
        return None

    def check_competition_period(self, request):
        """
        Checks if we are still in the competition. If the user is logged in,
        they are redirected to a competition status page.
        """
        if request.user.is_authenticated():
            path = request.path

            staff_user = request.user.is_staff or request.session.get('staff',
                                                                      False)
            if not staff_user:
                pattern = re.compile("^/"
                                     "(m\/|home\/restricted|site_media|media|"
                                     "favicon.ico)/")
                if not pattern.match(path):
                    if not in_competition():
                        return HttpResponseRedirect(reverse("home_restricted"))
        return None
