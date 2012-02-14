from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^$', "pages.views.index", name="help_index"),
    url(r'^(?P<category>\w+)/(?P<slug>[\w\d\-]+)/$', 'widgets.help.views.topic', name='help_topic'),
)
