"""Admin definition."""
from django.contrib import admin
from apps.widgets.notifications.models import NoticeTemplate


admin.site.register(NoticeTemplate)
