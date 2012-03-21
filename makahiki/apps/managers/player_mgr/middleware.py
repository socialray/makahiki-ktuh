"""A middleware class for player login checking and tracking."""

import re
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from apps.managers.settings_mgr import in_competition
import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from apps.managers.settings_mgr.models import ChallengeSettings, RoundSettings, PageSettings


def _load_db_settings():
    """Load additional settings from DB."""

    # get the CALLENGE setting from DB
    settings.CHALLENGE, _ = ChallengeSettings.objects.get_or_create(pk=1)

    # required setting for the CAS authentication service.
    settings.CAS_SERVER_URL = settings.CHALLENGE.cas_server_url

    # global settings
    settings.LOCALE_SETTING = settings.CHALLENGE.locale_setting
    settings.TIME_ZONE = settings.CHALLENGE.time_zone
    settings.LANGUAGE_CODE = settings.CHALLENGE.language_code

    # email settings
    if settings.CHALLENGE.email_enabled:
        settings.EMAIL_HOST = settings.CHALLENGE.email_host
        settings.EMAIL_PORT = settings.CHALLENGE.email_port
        settings.EMAIL_HOST_USER = settings.CHALLENGE.email_host_user
        settings.EMAIL_HOST_PASSWORD = settings.CHALLENGE.email_host_password
        settings.EMAIL_USE_TLS = settings.CHALLENGE.email_use_tls

    # get the Round settings from DB
    rounds = RoundSettings.objects.all()
    if rounds.count() == 0:
        RoundSettings.objects.create()
        rounds = RoundSettings.objects.all()

    #store in a round dictionary and calculate start and end
    rounds_dict = {}
    settings.COMPETITION_START = None
    last_round = None
    for competition_round in rounds:
        if settings.COMPETITION_START is None:
            settings.COMPETITION_START = competition_round.start
        rounds_dict[competition_round.name] = {
            "start": competition_round.start,
            "end": competition_round.end, }
        last_round = competition_round
    if last_round:
        settings.COMPETITION_END = last_round.end
    settings.COMPETITION_ROUNDS = rounds_dict

    # register the home page and widget
    PageSettings.objects.get_or_create(name="home", widget="home")


def _create_admin_user():
    """Create admin user.

    Create the admin user if not exists. otherwise, reset the password to the ENV.
    """
    print settings.ADMIN_USER
    try:
        user = User.objects.get(username=settings.ADMIN_USER)
        if not user.check_password(settings.ADMIN_PASSWORD):
            user.set_password(settings.ADMIN_PASSWORD)
            user.save()
    except ObjectDoesNotExist:
        user = User.objects.create_superuser(settings.ADMIN_USER, "", settings.ADMIN_PASSWORD)
        profile = user.get_profile()
        profile.setup_complete = True
        profile.setup_profile = True
        profile.completion_date = datetime.datetime.today()
        profile.save()


class LoginMiddleware(object):
    """This middleware does the following checks and tracking:
         * checks if today is in the competition period
         * checks if user has completed the setup
         * tracks how many days in a row the user has come to the site.
    """

    def process_request(self, request):
        """Check the competition period and that setup is completed."""

        # load the db settings if not done yet.
        if settings.CHALLENGE.competition_name is None:
            _load_db_settings()
            _create_admin_user()

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
                    if not in_competition():
                        return HttpResponseRedirect(reverse("home_restricted"))
        return None
