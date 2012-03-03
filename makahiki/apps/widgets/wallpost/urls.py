"""urls"""
from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^more_posts/$', 'widgets.wallpost.views.more_posts', name='news_more_posts'),
    url(r'^post/$', 'widgets.wallpost.views.post', name="news_post"),
)
