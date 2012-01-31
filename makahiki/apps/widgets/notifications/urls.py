from django.conf.urls.defaults import *

urlpatterns = patterns('widgets.notifications.views',
    url(r'^(\d+)/read/$', 'read', name="notifications_read"),
)
