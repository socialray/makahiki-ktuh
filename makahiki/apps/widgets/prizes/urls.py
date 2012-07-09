"""urls for raffle widget"""
from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^(\d+)/view-form/$', 'apps.widgets.prizes.views.prize_form',
        name="prize_view_form"),
)
