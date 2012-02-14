from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    #url(r'^$', 'widgets.energy.views.index', name='energy_index'),
    url(r'^$', 'pages.views.index', name='energy_index'),
    url(r'^vote/(?P<goal_id>\d+)/$', 'widgets.energy.views.vote', name='goal_vote'),
    url(r'^vote/(?P<goal_id>\d+)/results/$', 'widgets.energy.views.voting_results',
        name='goal_vote_results'),
)
