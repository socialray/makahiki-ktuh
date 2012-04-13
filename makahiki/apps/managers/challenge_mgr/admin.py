"""Implements the admin interface for game settings."""
from django.contrib import admin
from apps.managers.challenge_mgr.models import ChallengeSettings, RoundSettings, PageSettings


class PageSettingsAdmin(admin.ModelAdmin):
    """PageSettings administrator interface definition."""
    list_display = ["name", "widget", "enabled"]

admin.site.register(PageSettings, PageSettingsAdmin)


class RoundSettingsAdmin(admin.ModelAdmin):
    """PageSettings administrator interface definition."""
    list_display = ["name", "start", "end"]

admin.site.register(RoundSettings, RoundSettingsAdmin)

admin.site.register(ChallengeSettings)
