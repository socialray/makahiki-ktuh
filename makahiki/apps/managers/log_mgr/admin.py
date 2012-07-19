"""log model admin."""
from django.contrib import admin
from django.db import models
from django.forms.widgets import TextInput
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.log_mgr.models import MakahikiLog


class MakahikiLogAdmin(admin.ModelAdmin):
    """admin"""
    list_display = ('request_url', "remote_user", 'remote_ip', 'request_time', 'response_status')
    list_filter = ('remote_user', 'remote_ip', 'response_status')
    search_fields = ('request_url',)
    ordering = ["-request_time"]
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})},
        }

admin.site.register(MakahikiLog, MakahikiLogAdmin)
challenge_mgr.register_sys_admin_model("Logs", MakahikiLog)
