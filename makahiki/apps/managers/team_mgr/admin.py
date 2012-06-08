"""Administrator interface to teams."""
from django.contrib import admin
from apps.managers.team_mgr.models import Group, Team, Post


class GroupAdmin(admin.ModelAdmin):
    """Category Admin"""
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Group, GroupAdmin)


class TeamAdmin(admin.ModelAdmin):
    """Category Admin"""
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Team, TeamAdmin)


class PostAdmin(admin.ModelAdmin):
    """Post administrator for teams, overrides delete_selected"""
    list_filter = ["style_class", "team"]
    actions = ["delete_selected"]

    def delete_selected(self, request, queryset):
        """delete selected override"""
        _ = request
        for obj in queryset:
            obj.delete()

    delete_selected.short_description = "Delete the selected objects."

admin.site.register(Post, PostAdmin)
