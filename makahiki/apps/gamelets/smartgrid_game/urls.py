from django.conf.urls.defaults import *

urlpatterns = patterns('',

    url(r'^(?P<activity_type>[\w]+)/(?P<slug>[\w\d\-]+)/$', 'gamelets.smartgrid_game.views.task', name='activity_task'),
    url(r'^(?P<activity_type>[\w]+)/(?P<slug>[\w\d\-]+)/add/$', 'gamelets.smartgrid_game.views.add_task', name='activity_add_task'),
    url(r'^(?P<activity_type>[\w]+)/(?P<slug>[\w\d\-]+)/drop/$', 'gamelets.smartgrid_game.views.drop_task', name='activity_drop_task'),
    
    url(r'^(?P<activity_type>[\w]+)/(?P<slug>[\w\d\-]+)/codes/$', 'gamelets.smartgrid_game.views.view_codes', name='activity_view_codes'),

    url(r'^attend_code/$', 'gamelets.smartgrid_game.views.attend_code', name="activity_attend_code"),
    url(r'^(?P<activity_type>[\w]+)/(?P<slug>[\w\d\-]+)/reminder/$', 'gamelets.smartgrid_game.views.reminder', name='activity_reminder'),
    url(r'^(?P<activity_type>[\w]+)/(?P<slug>[\w\d\-]+)/rsvps/$', 'gamelets.smartgrid_game.views.view_rsvps', name='activity_view_rsvps'),
)
