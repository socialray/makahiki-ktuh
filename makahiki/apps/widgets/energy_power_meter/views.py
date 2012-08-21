"""Handle rendering of the Energy Power Meter widget."""
from apps.widgets.resource_goal import resource_goal


def supply(request, page_name):
    """Return the view_objects content, which in this case is empty."""

    _ = page_name

    team = request.user.get_profile().team
    if team:
        interval = resource_goal.team_goal_settings(team, "energy").realtime_meter_interval
    else:
        interval = None
    width = 300
    height = 100
    return {"interval": interval,
            "width": width,
            "height": height
            }
