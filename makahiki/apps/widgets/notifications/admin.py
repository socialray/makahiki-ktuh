"""Admin definition."""
from django.contrib import admin
from apps.managers.challenge_mgr import challenge_mgr
from apps.widgets.notifications.models import NoticeTemplate, UserNotification
from apps.admin.admin import challenge_designer_site, challenge_manager_site, developer_site


class UserNotificationAdmin(admin.ModelAdmin):
    """raffle admin"""
    list_display = ('recipient', 'content_object', 'content_type', 'unread', 'level')
    search_fields = ('recipient__username', 'content_type__name')


admin.site.register(NoticeTemplate)
challenge_designer_site.register(NoticeTemplate)
challenge_manager_site.register(NoticeTemplate)
developer_site.register(NoticeTemplate)
admin.site.register(UserNotification, UserNotificationAdmin)
challenge_designer_site.register(UserNotification, UserNotificationAdmin)
challenge_manager_site.register(UserNotification, UserNotificationAdmin)
developer_site.register(UserNotification, UserNotificationAdmin)
challenge_mgr.register_designer_challenge_info_model("Other Settings", 3, NoticeTemplate, 3)
challenge_mgr.register_admin_challenge_info_model("Notifications", 3, UserNotification, 2)
challenge_mgr.register_developer_challenge_info_model("Status", 4, NoticeTemplate, 5)
challenge_mgr.register_developer_challenge_info_model("Status", 4, UserNotification, 5)
