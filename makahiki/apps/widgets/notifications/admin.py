"""Admin definition."""
from django.contrib import admin
from apps.managers.challenge_mgr import challenge_mgr
from apps.widgets.notifications.models import NoticeTemplate, UserNotification


class UserNotificationAdmin(admin.ModelAdmin):
    """raffle admin"""
    list_display = ('recipient', 'unread', 'level')


admin.site.register(NoticeTemplate)
admin.site.register(UserNotification, UserNotificationAdmin)
challenge_mgr.register_sys_admin_model("Notifications", NoticeTemplate)
challenge_mgr.register_sys_admin_model("Notifications", UserNotification)
