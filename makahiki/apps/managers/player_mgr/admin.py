"""Defines the class for administration of players."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
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
    list_display = ['name', 'last_name', 'first_name', 'team', 'points', 'setup_complete', 'is_ra',
                    'user_link']

    inlines = [BadgeInline]

    def last_name(self, obj):
        """return the user last_name."""
        return obj.user.last_name
    last_name.short_description = 'Last_name'

    def first_name(self, obj):
        """return the user first_name."""
        return obj.user.first_name
    first_name.short_description = 'First_name'

    def points(self, obj):
        """return the user first_name."""
        return obj.points()
    points.short_description = 'Points'


admin.site.register(Profile, ProfileAdmin)
challenge_mgr.register_site_admin_model("Players", Profile)


class MakahikiUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'team', 'is_staff')

    def team(self, obj):
        """return the user last_name."""
        return obj.get_profile().team
    team.short_description = 'Team'


admin.site.unregister(User)
admin.site.register(User, MakahikiUserAdmin)
challenge_mgr.register_site_admin_model("Players", User)
