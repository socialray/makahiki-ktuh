"""A middleware class for player login checking and tracking."""

import re
import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from apps.managers.challenge_mgr import challenge_mgr


class LoginMiddleware(object):
    """This middleware does the following checks and tracking:
         * checks if today is in the competition period
         * checks if user has completed the setup
         * tracks how many days in a row the user has come to the site.
    """

    def process_request(self, request):
        """Check the competition period and that setup is completed."""

        # load the db settings if not done yet.
        challenge_mgr.init()

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
        """ Check to see if setup has been completed."""
        user = request.user
        path = request.path
        if user.is_authenticated():
            profile = user.get_profile()

            # We need to check if the user is going to the home page so we don't
            # get caught in a redirect loop. We do need to filter out requests
            # for CSS and other resources.
            pattern = re.compile("^/"
                                 "(m\/admin|m\/setup|admin|log|account|home|"
                                 "site_media|tc|media|favicon.ico)/")
            if not profile.setup_complete and not pattern.match(path):
                return HttpResponseRedirect("/")

        return None

    def check_competition_period(self, request):
        """Checks if we are still in the competition. If the user is logged in,
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
                    if not challenge_mgr.in_competition():
                        return HttpResponseRedirect(reverse("home_restricted"))
        return None
