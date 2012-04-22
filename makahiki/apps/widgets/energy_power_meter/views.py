"""Handle rendering of the Energy Power Meter widget."""

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from apps.lib.gviz_api import gviz_api
from apps.widgets.energy_power_meter.models import PowerData


def supply(request, page_name):
    """Return the view_objects content, which in this case is empty."""

    _ = request
    _ = page_name
    return {None:None}


@login_required
def power_data(request):
    """Return the gviz json data for power."""
    user = request.user

    description = {"A": ("string", "Source"),
                   "B": ("date", "Last Update"),
                   "C": ("number", "Current Power"),
                   "D": ("number", "Baseline Power")}

    # Loading it into gviz_api.DataTable
    data_table = gviz_api.DataTable(description)

    try:
        power = PowerData.objects.get(team=user.get_profile().team)
        data = [{"A": power.team.name,
                 "B": power.updated_at,
                 "C": power.current_power,
                 "D": power.baseline_power,
            }]

        data_table.AppendData(data)
    except ObjectDoesNotExist:
        pass

    return HttpResponse(data_table.ToResponse(tqx="reqId:0"))
