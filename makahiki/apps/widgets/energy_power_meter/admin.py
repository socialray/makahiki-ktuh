"""Administrator interface to energy power meter, displaying team, current power, and baseline."""
from django.contrib import admin

from apps.widgets.energy_power_meter.models import PowerData


class PowerDataAdmin(admin.ModelAdmin):
    """Specifies admin interface display list."""
    list_display = ["team", "current_power", "baseline_power"]

admin.site.register(PowerData, PowerDataAdmin)
