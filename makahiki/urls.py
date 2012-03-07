"""Defines the Main URLS."""

import os
import datetime
from django.conf import settings
from django.conf.urls.defaults import url, patterns, include
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.simple import direct_to_template
from apps.managers.settings_mgr.models import ChallengeSettings, RoundSettings, PageSettings

admin.autodiscover()

urlpatterns = patterns('',
    # Main page.
    url(r'^$', "apps.pages.views.root_index", name="root_index"),

    # page urls
    url(r'^home/$', "apps.pages.views.index", name="home_index"),
    url(r'^help/$', "apps.pages.views.index", name="help_index"),
    url(r'^learn/$', "apps.pages.views.index", name="learn_index"),
    url(r'^profile/$', "apps.pages.views.index", name="profile_index"),
    url(r'^energy/$', "apps.pages.views.index", name="energy_index"),
    url(r'^news/$', "apps.pages.views.index", name="news_index"),
    url(r'^win/$', "apps.pages.views.index", name="win_index"),
    url(r'^canopy/$', 'apps.pages.views.index', name="canopy_index"),

    # system level
    url(r'^log/', include('apps.managers.log_mgr.urls')),
    url(r'^help/', include('apps.widgets.help.urls')),
    url(r'^avatar/', include('apps.lib.avatar.urls')),


    url(r'^account/cas/login/$', 'apps.lib.django_cas.views.login', name='cas_login'),
    url(r'^account/cas/logout/$', 'apps.lib.django_cas.views.logout', name='cas_logout'),
    url(r'^account/login/$', 'apps.managers.auth_mgr.views.login', name='auth_login'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/login-as/(?P<user_id>\d+)/$', 'apps.managers.auth_mgr.views.login_as', name='auth_login_as'),
    url(r'^admin/logout/$', 'apps.managers.auth_mgr.views.logout', name='auth_logout'),

    url(r'^landing/$', direct_to_template, {'template': 'landing.html'}, name='landing'),
    url(r'^restricted/$', direct_to_template, {"template": 'restricted.html'}, name="restricted"),
    url(r'^about/$', direct_to_template, {'template': 'about.html'}, name='about'),
    url(r'^browser-check/$', direct_to_template, {'template': 'browser_check.html'},
        name='browser_check'),
    url(r'^coming-soon/$', direct_to_template, {'template': 'coming_soon.html'},
        name='coming_soon'),
    )

for widget in settings.INSTALLED_WIDGET_APPS:
    if os.path.isfile(
        "%s/apps/widgets/%s/urls.py" % (settings.PROJECT_ROOT, widget)):
        urlpatterns += patterns('',
            (r'^%s/' % widget, include('widgets.%s.urls' % widget)), )

if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        (r'^site_media/', include('staticfiles.urls')),
                            )


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
    try:
        user = User.objects.get(username=settings.ADMIN_USER)
        user.set_password(settings.ADMIN_PASSWORD)
        user.save()
    except ObjectDoesNotExist:
        user = User.objects.create_superuser(settings.ADMIN_USER, "", settings.ADMIN_PASSWORD)
        profile = user.get_profile()
        profile.setup_complete = True
        profile.setup_profile = True
        profile.completion_date = datetime.datetime.today()
        profile.save()

# load the db settings if not done yet.
if not hasattr(settings, "CHALLENGE"):
    _load_db_settings()

# create the admin user or reset the password from ENV
_create_admin_user()