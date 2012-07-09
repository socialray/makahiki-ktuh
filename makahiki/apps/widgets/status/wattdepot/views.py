"""Power meters visualization."""

from apps.widgets.viz_power_meters.views import remote_supply
from apps.widgets.resource_goal.models import EnergyGoalSetting


def supply(request, page_name):
    """ Call the remote viz request."""

    _ = page_name
    _ = request
    setting = EnergyGoalSetting.objects.all()[1]
    interval = setting.power_meter_interval
    return {
        "interval": interval,
        "data": remote_supply(request, page_name)
    }
