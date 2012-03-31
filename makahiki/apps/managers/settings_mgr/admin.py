"""Implements the admin interface for game settings."""
from django.contrib import admin
from apps.managers.settings_mgr.models import ChallengeSettings, RoundSettings, PageSettings

admin.site.register(ChallengeSettings)


class PageSettingsAdmin(admin.ModelAdmin):
    """PageSettings administrator interface definition."""
    list_display = ["name", "widget", "enabled"]

admin.site.register(PageSettings, PageSettingsAdmin)


class RoundSettingsAdmin(admin.ModelAdmin):
    """PageSettings administrator interface definition."""
    list_display = ["name", "start", "end"]

admin.site.register(RoundSettings, RoundSettingsAdmin)
