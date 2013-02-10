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
        """return the user overall points."""
        return obj.points()
    points.short_description = 'Points'


admin.site.register(Profile, ProfileAdmin)
#challenge_mgr.register_site_admin_model("Players", Profile)


class MakahikiUserAdmin(UserAdmin):
    """extends the UserAdmin for the user admin interface."""
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active',
                    'is_staff', "profile", 'team', 'referred_by')
    actions = ["set_active", "set_inactive"]

    def set_active(self, request, queryset):
        """set the active flag priority."""
        _ = request
        for obj in queryset:
            obj.is_active = True
            obj.save()
    set_active.short_description = "Activate the selected users."

    def set_inactive(self, request, queryset):
        """set the active flag priority."""
        _ = request
        for obj in queryset:
            obj.is_active = False
            obj.save()
    set_inactive.short_description = "Deactivate the selected users."

    def team(self, obj):
        """return the user name."""
        return obj.get_profile().team
    team.short_description = 'Team'

    def referred_by(self, obj):
        """return the name of the referrer."""
        return obj.get_profile().referring_user

    referred_by.short_description = 'Referred by'

    def profile(self, obj):
        """return the user profile."""
        return '<a href="%s/%d/">%s</a>' % ("/admin/player_mgr/profile",
                                           obj.get_profile().pk,
                                           obj.get_profile().name)
    profile.allow_tags = True
    profile.short_description = 'Link to Profile'


admin.site.unregister(User)
admin.site.register(User, MakahikiUserAdmin)
challenge_mgr.register_designer_challenge_info_model("Players", 2, User, 2)
