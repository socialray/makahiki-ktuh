"""log model admin."""
from django.contrib import admin
from django.db import models
from django.forms.widgets import TextInput
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.log_mgr.models import MakahikiLog
from apps.admin.admin import challenge_designer_site, challenge_manager_site, developer_site


class MakahikiLogAdmin(admin.ModelAdmin):
    """admin"""
    list_display = ('request_url', "remote_user", 'remote_ip', 'request_time',
                    'request_method', 'response_status')
    list_filter = ('response_status', 'remote_user')
    search_fields = ('request_url', 'remote_ip')
    ordering = ["-request_time"]
    date_hierarchy = "request_time"
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})},
        }

    def has_add_permission(self, request):
        return False

admin.site.register(MakahikiLog, MakahikiLogAdmin)
challenge_designer_site.register(MakahikiLog, MakahikiLogAdmin)
challenge_manager_site.register(MakahikiLog, MakahikiLogAdmin)
developer_site.register(MakahikiLog, MakahikiLogAdmin)
challenge_mgr.register_admin_challenge_info_model("Status", 1, MakahikiLog, 1)
challenge_mgr.register_developer_challenge_info_model("Status", 4, MakahikiLog, 1)
