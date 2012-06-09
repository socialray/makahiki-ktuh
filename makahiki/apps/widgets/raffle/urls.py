"""urls for raffle widget"""
from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^raffle/(\d+)/add_ticket/$', 'apps.widgets.raffle.views.add_ticket',
        name="raffle_add_ticket"),
    url(r'^raffle/(\d+)/remove_ticket/$', 'apps.widgets.raffle.views.remove_ticket',
        name="raffle_remove_ticket"),
    url(r'^raffle/(\d+)/view-form/$', 'apps.widgets.raffle.views.raffle_form',
        name="raffle_view_form"),
    url(r'^raffle/prize_list/$', 'apps.widgets.raffle.views.raffle_prize_list',
        name="raffle_prize_list"),
)
