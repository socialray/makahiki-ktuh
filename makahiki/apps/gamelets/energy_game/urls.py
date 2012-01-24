from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^vote/(?P<goal_id>\d+)/$', 'gamelets.energy_game.views.vote', name='goal_vote'),
    url(r'^vote/(?P<goal_id>\d+)/results/$', 'gamelets.energy_game.views.voting_results', name='goal_vote_results'),
)
