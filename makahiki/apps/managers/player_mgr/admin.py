"""Defines the class for administration of players."""
from django.contrib import admin
from django.contrib.auth.models import User
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.player_mgr.models import Profile
from apps.widgets.badges.models import BadgeAward
from django.forms.models import BaseInlineFormSet


class BadgeAwardFormSet(BaseInlineFormSet):
    """Custom formset model to override validation."""

    def clean(self):
        """Validates the form data and checks if the activity confirmation type is text."""


class BadgeInline(admin.TabularInline):
    """Badge admin."""
    model = BadgeAward
    fieldset = (
        (None, {
            'fields': ('badge'),
            })
        )

    extra = 1
    formset = BadgeAwardFormSet


class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for Profiles."""
    search_fields = ["user__username", "user__email"]
    list_display = ['name', 'last_name', 'first_name', ]
    inlines = [BadgeInline]
admin.site.register(Profile, ProfileAdmin)
challenge_mgr.register_site_admin_model("Players", Profile)
challenge_mgr.register_site_admin_model("Players", User)
