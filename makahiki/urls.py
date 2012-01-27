from django.conf.urls.defaults import *
from django.conf import settings

from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

import os

urlpatterns = patterns('',
    # Main pages.
    url(r'^$', "pages.views.root_index", name="root_index"),

    url(r'^getnutz', "pages.views.index", name = "getnutz_index"),
    url(r'^energy', "pages.views.index", name = "energy_index"),
    url(r'^news', "pages.views.index", name = "news_index"),
    url(r'^prizes', "pages.views.index", name = "prizes_index"),
    url(r'^profile', "pages.views.index", name = "profile_index"),
    url(r'^help', "pages.views.index", name = "help_index"),

    url(r'^getnutz/', include('gamelets.smartgrid_game.urls')),

    # system level
    url(r'^home/', include('pages.home.urls')),
    url(r'^landing/$', direct_to_template, {'template': 'pages/templates/landing.html'}, name='landing'),
    url(r'^restricted/$', direct_to_template, {"template": 'pages/templates/restricted.html'}, name="restricted"),
    url(r'^about/$', direct_to_template, {'template': 'pages/templates/about.html'}, name='about'),
    url(r'^browser-check/$', direct_to_template, {'template': 'pages/templates/browser_check.html'}, name='browser_check'),
    url(r'^coming-soon/$', direct_to_template, {'template': 'pages/templates/coming_soon.html'}, name='coming_soon'),

    # service views.
    url(r'^account/cas/login/$', 'lib.django_cas.views.login'),
    url(r'^account/cas/logout/$', 'lib.django_cas.views.logout'),
#    url(r'^ask-admin/', include('components.ask_admin.urls')),
#    url(r'^avatar/', include('components.makahiki_avatar.urls')),
    # url(r'^resources/', include('components.resources.urls')),
#    url(r'^themes/', include('components.makahiki_themes.urls')),
#    url(r'^quest/', include('components.quests.urls')),
#    url(r'^notifications/', include('components.makahiki_notifications.urls')),
#    url(r'^log/', include('components.logging.urls')),

    # 3rd party
#    (r'^frontendadmin/', include('frontendadmin.urls')),
#    (r'^attachments/', include('attachments.urls')),
#    (r'^sentry/', include('sentry.urls')),

    # pinax provided
    # (r'^account/', include('account.urls')),
#    (r'^admin/status/', include('pages.status.urls'),),
    (r'^admin/login-as/(?P<user_id>\d+)/$', 'services.auth_mgr.views.login_as'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    # (r'^notifications/', include('notification.urls')),

)

if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        (r'^site_media/', include('staticfiles.urls')),
    )
