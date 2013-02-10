"""Admin definition."""
from django.contrib import admin
from apps.managers.challenge_mgr import challenge_mgr
from apps.widgets.notifications.models import NoticeTemplate, UserNotification


class UserNotificationAdmin(admin.ModelAdmin):
    """raffle admin"""
    list_display = ('recipient', 'content_object', 'content_type', 'unread', 'level')
    search_fields = ('recipient__username', 'content_type__name')


admin.site.register(NoticeTemplate)
admin.site.register(UserNotification, UserNotificationAdmin)
challenge_mgr.register_designer_challenge_info_model("Other Settings", 3, NoticeTemplate, 3)
challenge_mgr.register_admin_challenge_info_model("Notifications", 3, UserNotification, 2)
