"""
urls for ask admin
"""
#pylint: disable=C0103
from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^send-feedback/$',
        'widgets.ask_admin.views.send_feedback', name="ask_admin_feedback"),
)
