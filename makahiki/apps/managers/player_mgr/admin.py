"""Defines the class for administration of players."""

from django.contrib import admin
from apps.managers.player_mgr.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for Profiles."""
    search_fields = ["user__username", "user__email"]
    list_display = ['name', 'last_name', 'first_name', ]

admin.site.register(Profile, ProfileAdmin)
