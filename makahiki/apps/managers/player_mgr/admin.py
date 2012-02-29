"""
Player Manager Admin
"""
from django.contrib import admin
from apps.managers.player_mgr.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    """
    Admin config for Profile
    """
    search_fields = ["user__username", "user__email"]
    list_display = ['name', 'last_name', 'first_name', ]

admin.site.register(Profile, ProfileAdmin)
