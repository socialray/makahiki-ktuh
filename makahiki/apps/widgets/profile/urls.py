from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    #url(r'^username_autocomplete/$', 'autocomplete_app.views.username_autocomplete_friends', name='profile_username_autocomplete'),
    #url(r'^username_autocomplete/$', 'autocomplete_app.views.username_autocomplete_all', name='profile_username_autocomplete'),
    #url(r'^$', 'player_mgr.views.profiles', name='profile_list'),
    url(r'^$', "pages.views.index", name="profile_index"),
    url(r'^badges/$', 'widgets.profile.views.badge_catalog', name="profile_badges"),
    url(r'^view_rejected/(\d+)/$', 'widgets.profile.views.view_rejected', name="profile_rejected"),
)
