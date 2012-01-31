from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^vote/(?P<goal_id>\d+)/$', 'widgets.energy.views.vote', name='goal_vote'),
    url(r'^vote/(?P<goal_id>\d+)/results/$', 'widgets.energy.views.voting_results', name='goal_vote_results'),
)
