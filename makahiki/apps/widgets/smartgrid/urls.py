from django.conf.urls.defaults import *

urlpatterns = patterns('',

    url(r'^(?P<activity_type>[\w]+)/(?P<slug>[\w\d\-]+)/$', 'widgets.smartgrid.views.task', name='activity_task'),
    url(r'^(?P<activity_type>[\w]+)/(?P<slug>[\w\d\-]+)/add/$', 'widgets.smartgrid.views.add_task', name='activity_add_task'),
    url(r'^(?P<activity_type>[\w]+)/(?P<slug>[\w\d\-]+)/drop/$', 'widgets.smartgrid.views.drop_task', name='activity_drop_task'),
    
    url(r'^(?P<activity_type>[\w]+)/(?P<slug>[\w\d\-]+)/codes/$', 'widgets.smartgrid.views.view_codes', name='activity_view_codes'),

    url(r'^attend_code/$', 'widgets.smartgrid.views.attend_code', name="activity_attend_code"),
    url(r'^(?P<activity_type>[\w]+)/(?P<slug>[\w\d\-]+)/reminder/$', 'widgets.smartgrid.views.reminder', name='activity_reminder'),
    url(r'^(?P<activity_type>[\w]+)/(?P<slug>[\w\d\-]+)/rsvps/$', 'widgets.smartgrid.views.view_rsvps', name='activity_view_rsvps'),
)
