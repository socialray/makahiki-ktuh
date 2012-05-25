"""log model admin."""
from django.contrib import admin
from django.db import models
from django.forms.widgets import TextInput
from apps.managers.log_mgr.models import MakahikiLog


class MakahikiLogAdmin(admin.ModelAdmin):
    """admin"""
    list_display = ('request_url', "remote_user", 'remote_ip', 'request_time', 'response_status')
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})},
        }

admin.site.register(MakahikiLog, MakahikiLogAdmin)
