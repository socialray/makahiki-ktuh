"""urls"""
from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    # User Directory urls
    url(r'members/$', 'apps.widgets.canopy_member.views.members', name="canopy_members"),
)
