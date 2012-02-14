from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^$', 'pages.views.index', name='prizes_index'),
    url(r'^raffle/(\d+)/add_ticket/$', 'widgets.prizes.views.add_ticket', name="raffle_add_ticket"),
    url(r'^raffle/(\d+)/remove_ticket/$', 'widgets.prizes.views.remove_ticket',
        name="raffle_remove_ticket"),
    url(r'^raffle/(\d+)/view-form/$', 'widgets.prizes.views.raffle_form', name="raffle_view_form"),
)
