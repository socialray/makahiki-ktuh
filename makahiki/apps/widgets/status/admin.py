"""daily status widget administrator interface"""

from django.contrib import admin
from apps.widgets.status.models import DailyStatus
from apps.managers.challenge_mgr import challenge_mgr
from apps.admin.admin import challenge_designer_site, challenge_manager_site, developer_site


class DailyStatusAdmin(admin.ModelAdmin):
    """EnergyGoal administrator interface definition."""
    list_display = ["short_date", "daily_visitors", "setup_users", "updated_at"]
    ordering = ["-date"]

admin.site.register(DailyStatus, DailyStatusAdmin)
challenge_designer_site.register(DailyStatus, DailyStatusAdmin)
challenge_manager_site.register(DailyStatus, DailyStatusAdmin)
developer_site.register(DailyStatus, DailyStatusAdmin)
challenge_mgr.register_developer_challenge_info_model("Status", 3, DailyStatus, 7)
