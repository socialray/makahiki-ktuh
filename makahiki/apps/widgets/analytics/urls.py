from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'widgets.analytics.views.home', name='status_home'),
    url(r'^points/$', 'widgets.analytics.views.points_scoreboard', name='status_points'),
    url(r'^energy/$', 'widgets.analytics.views.energy_scoreboard', name='status_energy'),
    url(r'^users/$', 'widgets.analytics.views.users', name='status_users'),
    url(r'^prizes/$', 'widgets.analytics.views.prizes', name='status_prizes'),
    url(r'^activities/$', 'widgets.analytics.views.popular_activities', name='status_activities'),
    url(r'^rsvps/$', 'widgets.analytics.views.event_rsvps', name='status_rsvps'),
)
