"""urls for serving power data"""
from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^data/$', 'widgets.energy_power_meter.views.power_data', name="power_data"),
)
