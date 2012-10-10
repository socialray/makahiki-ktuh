"""urls definition for status widget."""

from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^analysis/$',
        'apps.widgets.status.views.analysis',
        name="status_analysis"),
    )
