"""
urls for help widgets
"""
#pylint: disable=C0103
from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^(?P<category>\w+)/(?P<slug>[\w\d\-]+)/$', 'managers.help_mgr.views.topic',
        name='help_topic'),
)
