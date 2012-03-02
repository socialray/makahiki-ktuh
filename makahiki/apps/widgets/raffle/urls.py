"""urls for raffle widget"""
from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^raffle/(\d+)/add_ticket/$', 'widgets.raffle.views.add_ticket', name="raffle_add_ticket"),
    url(r'^raffle/(\d+)/remove_ticket/$', 'widgets.raffle.views.remove_ticket',
        name="raffle_remove_ticket"),
    url(r'^raffle/(\d+)/view-form/$', 'widgets.raffle.views.raffle_form', name="raffle_view_form"),
)
