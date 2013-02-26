"""Implements the admin interface for game settings."""
from django.contrib import admin
from django.db import models
from django import forms
from django.forms.util import ErrorList
from django.forms.widgets import Textarea
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.challenge_mgr.models import ChallengeSetting, RoundSetting, PageSetting, \
    PageInfo, Sponsor, UploadImage, GameSetting, GameInfo, AboutPage
from apps.admin.admin import sys_admin_site, challenge_designer_site, challenge_manager_site, \
    developer_site


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


class DesignerPageInfoAdmin(admin.ModelAdmin):
    """Designer admin interface for PageInfo entries."""
    list_display = ["name", "unlock_condition", "priority"]

    fieldsets = (
        (None,
            {"fields":
                ("label",
                 "title",
                 "introduction",
                 "unlock_condition",
                 "priority",)
             }),
        )

    inlines = [PageSettingInline]

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 70})},
        }


admin.site.register(PageInfo, PageInfoAdmin)
challenge_designer_site.register(PageInfo, DesignerPageInfoAdmin)
challenge_manager_site.register(PageInfo, DesignerPageInfoAdmin)
developer_site.register(PageInfo, PageInfoAdmin)


class PageSettingAdmin(admin.ModelAdmin):
    """PageSetting administrator interface definition."""
    list_display = ["page", "widget", "enabled"]
    list_editable = ["widget", "enabled"]

admin.site.register(PageSetting, PageSettingAdmin)
challenge_designer_site.register(PageSetting, PageSettingAdmin)
challenge_manager_site.register(PageSetting, PageSettingAdmin)
developer_site.register(PageSetting, PageSettingAdmin)


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
challenge_designer_site.register(GameInfo, GameInfoAdmin)
challenge_manager_site.register(GameInfo, GameInfoAdmin)
developer_site.register(GameInfo, GameInfoAdmin)


class RoundSettingAdminForm(forms.ModelForm):
    """RoundSetting Admin Form."""
    class Meta:
        """Meta"""
        model = RoundSetting

    def clean(self):
        """validate the round date."""

        super(RoundSettingAdminForm, self).clean()

        # Data that has passed validation.
        cleaned_data = self.cleaned_data

        start = cleaned_data.get("start")
        end = cleaned_data.get("end")
        name = cleaned_data.get("name")

        # end date must be later than start date
        if end <= start:
            self._errors["end"] = ErrorList(
                [u"This end date must be later than the start date."])
            del cleaned_data["end"]

            return cleaned_data

        # can not overlap with other rounds
        for rs in RoundSetting.objects.all():
            if name != rs.name:
                if rs.start < start < rs.end:
                    self._errors["start"] = ErrorList(
                        [u"This date is overlapped with another round."])
                    del cleaned_data["start"]
                    break
                if rs.start < end < rs.end:
                    self._errors["end"] = ErrorList(
                        [u"This date is overlapped with another round."])
                    del cleaned_data["end"]
                    break
                if start < rs.start and rs.end < end:
                    self._errors["start"] = ErrorList(
                        [u"This date is overlapped with another round."])
                    del cleaned_data["start"]
                    self._errors["end"] = ErrorList(
                        [u"This date is overlapped with another round."])
                    del cleaned_data["end"]
                    break

        return cleaned_data


class RoundSettingAdmin(admin.ModelAdmin):
    """PageSetting administrator interface definition."""
    list_display = ["name", "start", "end", "round_reset", "display_scoreboard"]
    form = RoundSettingAdminForm


admin.site.register(RoundSetting, RoundSettingAdmin)
challenge_designer_site.register(RoundSetting, RoundSettingAdmin)
challenge_manager_site.register(RoundSetting, RoundSettingAdmin)
developer_site.register(RoundSetting, RoundSettingAdmin)


class SponsorsInline(admin.TabularInline):
    """SponsorsInline admin."""
    model = Sponsor
    extra = 0


class AboutPageInline(admin.StackedInline):
    """AboutPage inline admin"""
    model = AboutPage
    extra = 0

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 100})},
    }

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


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
                  (("name", "logo"),
                   ("domain", "theme"),
                   ("team_label", ),
                  )}),
        ("Landing Page",
            {"description": "<div class='help makahiki-box content-box-contents'>Setup the " + \
             "Landing Page. It is the first page players see.</div>",
             "fields":
                  ("landing_slogan",
                   "landing_introduction",
                   "landing_participant_text",
                   "landing_non_participant_text",)}),

    )

    inlines = [AboutPageInline, SponsorsInline]

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 70})},
        }

    page_text = "Click on the name of the challenge to change the settings." +\
    "There must be only one Challenge Setting."

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(ChallengeSetting, ChallengeSettingAdmin)
challenge_designer_site.register(ChallengeSetting, ChallengeSettingAdmin)
challenge_manager_site.register(ChallengeSetting, ChallengeSettingAdmin)
developer_site.register(ChallengeSetting, ChallengeSettingAdmin)
admin.site.register(UploadImage)
developer_site.register(UploadImage)

challenge_mgr.register_designer_challenge_info_model("Challenge", 1, ChallengeSetting, 1)
challenge_mgr.register_designer_challenge_info_model("Challenge", 1, RoundSetting, 2)
challenge_mgr.register_designer_challenge_info_model("Other Settings", 3, PageInfo, 1)

from djcelery.models import CrontabSchedule, PeriodicTask, IntervalSchedule
CrontabSchedule.__doc__ = "Defines the schedule in crontab format (minute/hour/day)."
developer_site.register(CrontabSchedule)

IntervalSchedule.__doc__ = "Defines the schedule in intervals, such as every hour, every minutes."
developer_site.register(IntervalSchedule)

PeriodicTask.__doc__ = "Defines the scheduled tasks."
developer_site.register(PeriodicTask)

challenge_mgr.register_developer_challenge_info_model("Challenge", 1, ChallengeSetting, 1)
challenge_mgr.register_developer_challenge_info_model("Challenge", 1, RoundSetting, 2)
admin.site.register(Sponsor)
developer_site.register(Sponsor)
challenge_mgr.register_developer_challenge_info_model("Challenge", 1, Sponsor, 3)
challenge_mgr.register_developer_challenge_info_model("Games", 3, GameInfo, 2)
challenge_mgr.register_developer_challenge_info_model("Games", 3, PageInfo, 1)
challenge_mgr.register_developer_challenge_info_model("Scheduler (Celery)", \
                                                      6, CrontabSchedule, 3)
challenge_mgr.register_developer_challenge_info_model("Scheduler (Celery)", \
                                                      6, IntervalSchedule, 3)
challenge_mgr.register_developer_challenge_info_model("Scheduler (Celery)", \
                                                      6, PeriodicTask, 1)
UploadImage.admin_tool_tip = "Uploaded images"
challenge_mgr.register_developer_challenge_info_model("Misc", 7, UploadImage, 1)
