"""urls for serving energy data"""
from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^data/$', 'widgets.energy_goal.views.energy_goal_data', name="energy_goal_data"),
)
