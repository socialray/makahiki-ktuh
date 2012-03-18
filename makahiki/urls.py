"""Defines the Main URLS."""

import os
from django.conf import settings
from django.conf.urls.defaults import url, patterns, include
from django.contrib import admin
from django.views.generic.simple import direct_to_template

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
    url(r'^water/$', "apps.pages.views.index", name="water_index"),
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
    url(r'^admin/login-as/(?P<user_id>\d+)/$', 'apps.managers.auth_mgr.views.login_as',
        name='auth_login_as'),
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
            (r'^%s/' % widget, include('apps.widgets.%s.urls' % widget)), )

if settings.SERVE_MEDIA:
    urlpatterns += patterns('', (r'^site_media/', include('staticfiles.urls')), )
