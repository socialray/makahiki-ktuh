from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^$', 'pages.views.index', name='news_index'),
    url(r'^more_posts/$', 'widgets.news.views.more_posts', name='news_more_posts'),
    url(r'^post/$', 'widgets.news.views.post', name="news_post"),
    url(r'^popular-tasks/$', 'widgets.news.views.get_popular_tasks', name="news_popular_tasks"),
    url(r'^team-members/$', 'widgets.news.views.team_members', name="news_team_members"),
)
