"""log model admin."""
from django.contrib import admin
from django.db import models
from django.forms.widgets import TextInput
from apps.managers.log_mgr.models import MakahikiLog


class MakahikiLogAdmin(admin.ModelAdmin):
    """admin"""
    list_display = ('remote_ip', "remote_user", 'request_url', 'request_time')
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})},
        }

admin.site.register(MakahikiLog, MakahikiLogAdmin)
