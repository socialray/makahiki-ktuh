from django.contrib import admin
from apps.lib.avatar.models import Avatar
from apps.managers.challenge_mgr import challenge_mgr
from apps.admin.admin import developer_site

admin.site.register(Avatar)
developer_site.register(Avatar)
Avatar.admin_tool_tip = "Player Avatars"
challenge_mgr.register_developer_challenge_info_model("Players", 2, Avatar, 4)
