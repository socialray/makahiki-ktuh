"""urls"""
from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^popular-tasks/$', 'widgets.popular_tasks.views.get_popular_tasks',
        name="news_popular_tasks"),
)
