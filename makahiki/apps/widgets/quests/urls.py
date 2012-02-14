from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)/accept/$', 'widgets.quests.views.accept', name="quests_accept"),
    url(r'^(?P<slug>[-\w]+)/opt-out/$', 'widgets.quests.views.opt_out', name="quests_opt_out"),
    url(r'^(?P<slug>[-\w]+)/cancel/$', 'widgets.quests.views.cancel', name="quests_cancel"),
)
