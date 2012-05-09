"""Implements the admin interface for game settings."""
from django.contrib import admin
from django.db import models
from django.forms.widgets import Textarea
from apps.managers.challenge_mgr.models import ChallengeSettings, RoundSettings, PageSettings, \
    PageInfo, Sponsor, UploadImage


class PageSettingsInline(admin.TabularInline):
    """PageSettingsInline admin."""
    model = PageSettings
    can_delete = False
    fields = ['widget', 'enabled', ]
    readonly_fields = ['widget', ]
    extra = 0

    def has_add_permission(self, request):
        return False


class PageInfoAdmin(admin.ModelAdmin):
    """PageSettings administrator interface definition."""
    list_display = ["name", "unlock_condition"]

    fieldsets = (
        (None,
            {"fields":
                  (("name", "label"),
                   "title",
                   "introduction",
                   "unlock_condition",
                   ("url", "priority"), )
            }),
    )

    inlines = [PageSettingsInline]

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 70})},
        }

admin.site.register(PageInfo, PageInfoAdmin)


class PageSettingsAdmin(admin.ModelAdmin):
    """PageSettings administrator interface definition."""
    list_display = ["page", "widget", "enabled"]
    list_editable = ["widget", "enabled"]

admin.site.register(PageSettings, PageSettingsAdmin)


class RoundSettingsAdmin(admin.ModelAdmin):
    """PageSettings administrator interface definition."""
    list_display = ["name", "start", "end"]

admin.site.register(RoundSettings, RoundSettingsAdmin)


class SponsorsInline(admin.TabularInline):
    """SponsorsInline admin."""
    model = Sponsor
    extra = 0


class ChallengeSettingsAdmin(admin.ModelAdmin):
    """ChallengeSettings administrator interface definition."""

    fieldsets = (
        (None,
            {"fields":
                  (("site_name", "site_logo"),
                   ("competition_name", "site_domain"),
                   "theme",
                   "competition_team_label",
                  )}),
        ("CAS or LDAP authentication",
            {"fields":
                  ("cas_server_url",
                   ("ldap_server_url", "ldap_search_base"), )}),
        ("Email",
             {"fields":
                  ("email_enabled",
                   "contact_email",
                   ("email_host", "email_port", "email_use_tls"), )}),
        ("Landing Page",
             {"fields":
                  ("landing_slogan",
                   "landing_introduction",
                   "landing_participant_text",
                   "landing_non_participant_text", )}),
    )

    inlines = [SponsorsInline]

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 70})},
        }

admin.site.register(ChallengeSettings, ChallengeSettingsAdmin)
admin.site.register(UploadImage)
