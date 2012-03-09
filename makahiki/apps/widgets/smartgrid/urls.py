"""urls definition for smartgrid widget."""

from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^(?P<activity_type>[\w]+)/(?P<slug>[\w\d\-]+)/$',
        'apps.widgets.smartgrid.views.view_task',
        name='activity_task'),
    url(r'^(?P<activity_type>[\w]+)/(?P<slug>[\w\d\-]+)/add/$',
        'apps.widgets.smartgrid.views.add_task',
        name='activity_add_task'),
    url(r'^(?P<activity_type>[\w]+)/(?P<slug>[\w\d\-]+)/drop/$',
        'apps.widgets.smartgrid.views.drop_task',
        name='activity_drop_task'),
    url(r'^(?P<activity_type>[\w]+)/(?P<slug>[\w\d\-]+)/codes/$',
        'apps.widgets.smartgrid.views.view_codes',
        name='activity_view_codes'),
    url(r'^attend_code/$',
        'apps.widgets.smartgrid.views.attend_code',
        name="activity_attend_code"),
    url(r'^(?P<activity_type>[\w]+)/(?P<slug>[\w\d\-]+)/reminder/$',
        'apps.widgets.smartgrid.views.reminder',
        name='activity_reminder'),
    url(r'^(?P<activity_type>[\w]+)/(?P<slug>[\w\d\-]+)/rsvps/$',
        'apps.widgets.smartgrid.views.view_rsvps',
        name='activity_view_rsvps'),
)
