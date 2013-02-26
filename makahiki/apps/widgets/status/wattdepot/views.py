"""Power meters visualization."""

from apps.widgets.resource_goal.models import EnergyGoalSetting
from apps.managers.team_mgr.models import Team


def supply(request, page_name):
    """ Call the remote viz request."""

    _ = page_name
    _ = request

    goal_settings = EnergyGoalSetting.objects.all()
    if goal_settings:
        setting = goal_settings[0]
        interval = setting.realtime_meter_interval
    else:
        interval = 10

    all_lounges = Team.objects.order_by('name').all()

    return {
        "interval": interval,
        "data": {"all_lounges": all_lounges, }
    }
