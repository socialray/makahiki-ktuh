"""A middleware class for player login checking and tracking."""

import re
import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from apps.managers.challenge_mgr import challenge_mgr
from apps.widgets.status.models import DailyStatus
from django.core.exceptions import ObjectDoesNotExist


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

        user = request.user
        if not user.is_authenticated():
            return None
        else:
            path = request.path

            # if user logged in and go to landing page, re-direct to home page
            if path.startswith("/landing/"):
                return HttpResponseRedirect(reverse("home_index"))

            # pass through for trivial requests
            pattern = "^/(home\/restricted|admin|about|log|account|site_media|favicon.ico)/"
            if re.compile(pattern).match(path):
                return None

        # now the user is authenticated and going to the non-trivial pages.
        response = self.check_competition_period(request)
        if response is None:
            response = self.check_setup_completed(request)
            if response is None:
                response = self.track_login(request)
                if response is None:
                    self.award_possible_badges(request)

        return response

    def track_login(self, request):
        """Checks if the user is logged in and updates the tracking field."""
        profile = request.user.get_profile()
        last_visit = request.user.get_profile().last_visit_date
        today = datetime.date.today()

        # Look for a previous login.
        if not last_visit:
            try:
                entry = DailyStatus.objects.get(date=today.isoformat())
                entry.daily_visitors = entry.daily_visitors + 1
            except ObjectDoesNotExist:
                entry = DailyStatus(date=today.isoformat(), daily_visitors=1)
            entry.save()

        if last_visit and (today - last_visit) == datetime.timedelta(days=1):
            profile.last_visit_date = today
            profile.daily_visit_count += 1
            profile.save()
            try:
                entry = DailyStatus.objects.get(date=today.isoformat())
                entry.daily_visitors = entry.daily_visitors + 1
            except ObjectDoesNotExist:
                entry = DailyStatus(date=today.isoformat(), daily_visitors=1)
            entry.save()
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
        profile = user.get_profile()

        # We need to check if the user is going to the home page so we don't
        # get caught in a redirect loop. We do need to filter out requests
        # for CSS and other resources.
        pattern = "^/(home|admin|log|about|account|tc|site_media|media|favicon.ico)/"

        if not profile.setup_complete and \
           not re.compile(pattern).match(path):
            return HttpResponseRedirect(reverse("home_index"))

        return None

    def check_competition_period(self, request):
        """Checks if we are still in the competition. If the user is logged in,
        they are redirected to a competition status page.
        """
        path = request.path
        pattern = "^/(home\/restricted|admin|about|log|account|site_media|media|favicon.ico)/"
        staff_user = request.user.is_staff or request.session.get('staff', False)

        if not staff_user and \
           not re.compile(pattern).match(path) and \
           not challenge_mgr.in_competition():
            return HttpResponseRedirect(reverse("home_restricted"))

        return None

    def award_possible_badges(self, request):
        """award any possible badges for a login user."""
        if "badges" in challenge_mgr.get_enabled_widgets():
            from apps.widgets.badges import badges
            badges.award_possible_badges(request.user)

        return None
