"""Ask Admin URL."""

from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^send-feedback/$',
        'apps.widgets.ask_admin.views.send_feedback', name="ask_admin_feedback"),
)
