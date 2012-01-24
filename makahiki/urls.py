from django.conf.urls.defaults import *
from django.conf import settings

from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

import os

urlpatterns = patterns('',
    # Main pages.
    url(r'^$', "pages.views.index", name="root_index"),

    url(r'^landing', "pages.views.index", name = "landing"),
    url(r'^home', "pages.views.index", name = "home_index"),
    url(r'^getnutz', "pages.views.index", name = "getnutz_index"),
    url(r'^energy', "pages.views.index", name = "energy_index"),
    url(r'^news', "pages.views.index", name = "news_index"),
    url(r'^prizes', "pages.views.index", name = "prizes_index"),
    url(r'^profile', "pages.views.index", name = "profile_index"),
    url(r'^help', "pages.views.index", name = "help_index"),

    url(r'^getnutz/', include('gamelets.smartgrid_game.urls')),

    url(r'^restricted/$', direct_to_template, {"template": 'gamelets/landing/templates/restricted.html'}, name="restricted"),
    url(r'^about/$', direct_to_template, {'template': 'gamelets/landing/templates/about.html'}, name='about'),
    url(r'^browser-check/$', direct_to_template, {'template': 'gamelets/landing/browser_check.html'}, name='browser_check'),
    url(r'^coming-soon/$', direct_to_template, {'template': 'gamelets/landing/coming_soon.html'}, name='coming_soon'),

)

if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        (r'^site_media/', include('staticfiles.urls')),
    )
