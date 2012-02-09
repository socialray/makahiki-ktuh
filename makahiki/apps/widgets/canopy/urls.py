from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'widgets.canopy.views.index', name="canopy_index"),
    
    # Quest URLS
    url(r'^mission/(?P<slug>[-\w]+)/accept/$', 'widgets.canopy.views.mission_accept', name="canopy_mission_accept"),
    # url(r'^quest/(?P<slug>[-\w]+)/opt-out/$', 'widgets.canopy.views.quest_opt_out', name="canopy_quest_opt_out"),
    url(r'^mission/(?P<slug>[-\w]+)/cancel/$', 'widgets.canopy.views.mission_cancel', name="canopy_mission_cancel"),
    
    # Wall URLS
    url(r'^wall/post/$', 'widgets.canopy.views.post', name="canopy_wall_post"),
    url(r'^wall/more-posts/$', 'widgets.canopy.views.more_posts', name="canopy_more_posts"),
    
    # User Directory urls
    url(r'members/$', 'widgets.canopy.views.members', name="canopy_members"),
)
