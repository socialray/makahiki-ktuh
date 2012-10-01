"""urls for raffle widget"""
from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^(\d+)/(\d+)/view-form/$', 'apps.widgets.prizes.views.prize_form',
        name="prize_view_form"),
    url(r'^(\d+)/view-form/$', 'apps.widgets.prizes.views.prize_team_winners',
        name="prize_team_winners"),
    url(r'^summary/(?P<round_name>[\w\d\-]+)/$', 'apps.widgets.prizes.views.prize_summary',
        name="prize_summary"),

)
