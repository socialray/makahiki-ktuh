from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'pages.views.index', name='news_index'),
    url(r'^more_posts/$', 'widgets.news.views.more_posts', name='news_more_posts'),
    url(r'^post/$', 'widgets.news.views.post', name="news_post"),
    url(r'^popular-tasks/$', 'widgets.news.views.get_popular_tasks', name="news_popular_tasks"),
    url(r'^floor-members/$', 'widgets.news.views.floor_members', name="news_floor_members"),
)
