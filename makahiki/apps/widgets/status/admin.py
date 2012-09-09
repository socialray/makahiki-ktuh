"""daily status widget administrator interface"""

from django.contrib import admin
from apps.managers.challenge_mgr import challenge_mgr
from apps.widgets.status.models import DailyStatus


class DailyStatusAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["short_date", "daily_visitors", "setup_users", "updated_at"]
    ordering = ["-date"]

admin.site.register(DailyStatus, DailyStatusAdmin)
challenge_mgr.register_sys_admin_model("Status", DailyStatus)
