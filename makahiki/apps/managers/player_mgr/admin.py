"""Defines the class for administration of players."""

from django.contrib import admin
from django.contrib.auth.models import User
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.player_mgr.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for Profiles."""
    search_fields = ["user__username", "user__email"]
    list_display = ['name', 'last_name', 'first_name', ]

admin.site.register(Profile, ProfileAdmin)
challenge_mgr.register_site_admin_model("Players", Profile)
challenge_mgr.register_site_admin_model("Players", User)
