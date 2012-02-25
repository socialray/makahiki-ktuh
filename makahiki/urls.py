import os
import types
from django.conf import settings
from django.conf.urls.defaults import url, patterns, include
from django.contrib import admin
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns('',
    # Main page.
    url(r'^$', "pages.views.root_index", name="root_index"),

    # page urls
    url(r'^home/$', "pages.views.index", name="home_index"),
    url(r'^help/$', "pages.views.index", name="help_index"),
    url(r'^actions/$', "pages.views.index", name="actions_index"),
    url(r'^profile/$', "pages.views.index", name="profile_index"),
    url(r'^energy/$', "pages.views.index", name="energy_index"),
    url(r'^news/$', "pages.views.index", name="news_index"),
    url(r'^prizes/$', "pages.views.index", name="prizes_index"),
    url(r'^canopy/$', 'pages.views.index', name="canopy_index"),

    # system level
    url(r'^log/', include('managers.log_mgr.urls')),
    url(r'^help/', include('managers.help_mgr.urls')),
    url(r'^account/login/$', 'managers.auth_mgr.views.login', name='auth_login'),
    url(r'^account/cas/login/$', 'lib.django_cas.views.login'),
    url(r'^account/cas/logout/$', 'lib.django_cas.views.logout'),
    url(r'^avatar/', include('lib.avatar.urls')),
    (r'^admin/login-as/(?P<user_id>\d+)/$', 'managers.auth_mgr.views.login_as'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    url(r'^landing/$', direct_to_template, {'template': 'landing.html'}, name='landing'),
    url(r'^restricted/$', direct_to_template, {"template": 'restricted.html'}, name="restricted"),
    url(r'^about/$', direct_to_template, {'template': 'about.html'}, name='about'),
    url(r'^browser-check/$', direct_to_template, {'template': 'browser_check.html'}, name='browser_check'),
    url(r'^coming-soon/$', direct_to_template, {'template': 'coming_soon.html'}, name='coming_soon'),
)

for widget_app in settings.INSTALLED_WIDGET_APPS:
    widget = widget_app.split('.')[1]
    if os.path.isfile("%s/apps/widgets/%s/urls.py" % (settings.PROJECT_ROOT, widget)):
        urlpatterns += patterns('', (r'^%s/' % widget, include('widgets.%s.urls' % widget)),)

if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        (r'^site_media/', include('staticfiles.urls')),
    )
