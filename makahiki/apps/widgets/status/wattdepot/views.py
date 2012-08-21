"""Power meters visualization."""

from apps.widgets.viz_power_meters.views import remote_supply
from apps.widgets.resource_goal.models import EnergyGoalSetting


def supply(request, page_name):
    """ Call the remote viz request."""

    _ = page_name
    _ = request

    goal_settings = EnergyGoalSetting.objects.all()
    if goal_settings:
        setting = goal_settings[1]
        interval = setting.realtime_meter_interval
    else:
        interval = 10

    return {
        "interval": interval,
        "data": remote_supply(request, page_name)
    }
