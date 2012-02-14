from django.conf import settings
from django.conf.urls.defaults import url, patterns, include
from django.contrib import admin
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns('',
    # Main page.
    url(r'^$', "pages.views.root_index", name="root_index"),

    # page urls
    url(r'^actions/', include('widgets.smartgrid.urls')),
    url(r'^profile/', include('widgets.profile.urls')),
    url(r'^help/', include('widgets.help.urls')),
    url(r'^energy/', include('widgets.energy.urls')),
    url(r'^news/', include('widgets.news.urls')),
    url(r'^prizes/', include('widgets.prizes.urls')),
    url(r'^canopy/', include('widgets.canopy.urls')),

    # system level
    url(r'^home/', include('pages.home.urls')),
    url(r'^landing/$', direct_to_template, {'template': 'landing.html'}, name='landing'),
    url(r'^restricted/$', direct_to_template, {"template": 'restricted.html'}, name="restricted"),
    url(r'^about/$', direct_to_template, {'template': 'about.html'}, name='about'),
    url(r'^browser-check/$', direct_to_template, {'template': 'browser_check.html'}, name='browser_check'),
    url(r'^coming-soon/$', direct_to_template, {'template': 'coming_soon.html'}, name='coming_soon'),

    # service views.
    url(r'^account/cas/login/$', 'lib.django_cas.views.login'),
    url(r'^account/cas/logout/$', 'lib.django_cas.views.logout'),

    url(r'^ask-admin/', include('widgets.ask_admin.urls')),
    url(r'^avatar/', include('managers.avatar_mgr.urls')),
    # url(r'^resources/', include('components.resources.urls')),
#    url(r'^themes/', include('components.makahiki_themes.urls')),
    url(r'^quest/', include('widgets.quests.urls')),
    url(r'^notifications/', include('widgets.notifications.urls')),
    url(r'^log/', include('managers.log_mgr.urls')),

    # 3rd party
#    (r'^frontendadmin/', include('frontendadmin.urls')),
#    (r'^attachments/', include('attachments.urls')),
#    (r'^sentry/', include('sentry.urls')),

    # (r'^account/', include('account.urls')),
    (r'^admin/status/', include('widgets.analytics.urls'),),
    (r'^admin/login-as/(?P<user_id>\d+)/$', 'managers.auth_mgr.views.login_as'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    # (r'^notifications/', include('notification.urls')),

)

if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        (r'^site_media/', include('staticfiles.urls')),
    )
