"""Admin definition."""
from django.contrib import admin
from apps.managers.challenge_mgr import challenge_mgr
from apps.widgets.notifications.models import NoticeTemplate, UserNotification


admin.site.register(NoticeTemplate)
admin.site.register(UserNotification)
challenge_mgr.register_sys_admin_model("Notifications", NoticeTemplate)
challenge_mgr.register_sys_admin_model("Notifications", UserNotification)
