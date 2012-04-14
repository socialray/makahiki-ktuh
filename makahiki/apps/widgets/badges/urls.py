"""urls"""
from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^badges/$', 'apps.widgets.badges.views.badge_catalog', name="profile_badges"),
)
