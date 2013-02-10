"""Implements the admin interface for game settings."""
from django.contrib import admin
from django.db import models
from django.forms.widgets import Textarea
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.challenge_mgr.models import ChallengeSetting, RoundSetting, PageSetting, \
    PageInfo, Sponsor, UploadImage, GameSetting, GameInfo
from apps.admin.admin import sys_admin_site, challenge_designer_site, challenge_manager_site


class PageSettingInline(admin.TabularInline):
    """PageSettingInline admin."""
    model = PageSetting
    # can_delete = False
    fields = ['widget', 'location', 'priority', 'enabled', ]
    # readonly_fields = ['widget', ]
    extra = 0

    # def has_add_permission(self, request):
    #    return False


class PageInfoAdmin(admin.ModelAdmin):
    """PageSetting administrator interface definition."""
    list_display = ["name", "unlock_condition", "priority"]

    fieldsets = (
        (None,
            {"fields":
                  (("name", "label"),
                   "title",
                   "introduction",
                   "unlock_condition",
                   ("url", "priority"),)
            }),
    )

    inlines = [PageSettingInline]

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 70})},
        }

admin.site.register(PageInfo, PageInfoAdmin)
challenge_designer_site.register(PageInfo, PageInfoAdmin)
challenge_manager_site.register(PageInfo, PageInfoAdmin)


class PageSettingAdmin(admin.ModelAdmin):
    """PageSetting administrator interface definition."""
    list_display = ["page", "widget", "enabled"]
    list_editable = ["widget", "enabled"]

admin.site.register(PageSetting, PageSettingAdmin)


class GameSettingInline(admin.TabularInline):
    """PageSettingInline admin."""
    model = GameSetting
    fields = ['widget', ]
    extra = 0


class GameInfoAdmin(admin.ModelAdmin):
    """PageSetting administrator interface definition."""
    list_display = ["name", "enabled", "priority"]
    fieldsets = (
        (None,
            {"fields":
                  (("name", "enabled"), "priority")
            }),
    )
    inlines = [GameSettingInline]

admin.site.register(GameInfo, GameInfoAdmin)


class RoundSettingAdmin(admin.ModelAdmin):
    """PageSetting administrator interface definition."""
    list_display = ["name", "start", "end", "round_reset", "display_scoreboard"]

admin.site.register(RoundSetting, RoundSettingAdmin)


class SponsorsInline(admin.TabularInline):
    """SponsorsInline admin."""
    model = Sponsor
    extra = 0


class SystemSettingAdmin(admin.ModelAdmin):
    """The system administrator's Challenge Administration interface definition."""
    fieldsets = (
        ("Authentication",
            {"description": "<div class='help makahiki-box content-box-contents'>Choose the " + \
             "type or types of authentication for players</div>",
             "fields":
                  (("use_cas_auth", "cas_server_url", "cas_auth_text"),
                   ("use_ldap_auth", "ldap_server_url", "ldap_search_base", "ldap_auth_text"),
                   ("use_internal_auth", "internal_auth_text"),
                  )}),
        ("WattDepot server for real time energy data",
            {"description": "<div class='help makahiki-box content-box-contents'>If using " + \
             "WattDepot for energy data, provide the WattDepot Server's URL.</div>",
             "fields":
                  ("wattdepot_server_url",)}),
        ("Email",
             {"description": "<div class='help makahiki-box content-box-contents'>If you want " + \
             "email notifications enable email and provide the host information.</div>",
             "fields":
                  ("email_enabled",
                   "contact_email",
                   ("email_host", "email_port", "email_use_tls"),)}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 70})},
        }
    page_text = "System Settings"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

sys_admin_site.register(ChallengeSetting, SystemSettingAdmin)


class ChallengeSettingAdmin(admin.ModelAdmin):
    """ChallengeSetting administrator interface definition."""

    fieldsets = (
        ("Challenge",
            {"description": "<div class='help makahiki-box content-box-contents'>Enter the " + \
             "information for this Challenge</div>",
             "fields":
                  (("name", "location"),
                   ("logo", "domain"),
                   ("team_label", "theme"),
                  )}),
        ("Landing Page",
            {"description": "<div class='help makahiki-box content-box-contents'>Setup the " + \
             "Landing Page. It is the first page players see.</div>",
             "fields":
                  ("landing_slogan",
                   "landing_introduction",
                   "landing_participant_text",
                   "landing_non_participant_text",)}),
        ("About Page",
            {"description": "<div class='help makahiki-box content-box-contents'>The " + \
             "About Page explains the Challenge.</div>",
             "fields":
                  ("about_page_text",)}),
    )

    inlines = [SponsorsInline]

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 70})},
        }
    page_text = "Click on the name of the challenge to change the settings."

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(ChallengeSetting, ChallengeSettingAdmin)
admin.site.register(UploadImage)

challenge_mgr.register_designer_challenge_info_model("Challenge", 1, ChallengeSetting, 1)
challenge_mgr.register_designer_challenge_info_model("Challenge", 1, RoundSetting, 2)
challenge_mgr.register_designer_challenge_info_model("Other Settings", 3, PageInfo, 1)

from djcelery.models import CrontabSchedule, PeriodicTask, IntervalSchedule
challenge_mgr.register_designer_challenge_info_model("Scheduler (Celery) - Optional", \
                                                     5, CrontabSchedule, 5)
challenge_mgr.register_designer_challenge_info_model("Scheduler (Celery) - Optional", \
                                                     5, IntervalSchedule, 5)
challenge_mgr.register_designer_challenge_info_model("Scheduler (Celery) - Optional", \
                                                     5, PeriodicTask, 5)
