"""Administrator interface to teams."""
from django.contrib import admin
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.team_mgr.models import Group, Team, Post
from apps.admin.admin import challenge_designer_site, challenge_manager_site, developer_site


class GroupAdmin(admin.ModelAdmin):
    """Category Admin"""
    list_display = ["name", ]
    page_text = "Groups are optional in this challenge."

admin.site.register(Group, GroupAdmin)
challenge_designer_site.register(Group, GroupAdmin)
challenge_manager_site.register(Group, GroupAdmin)
developer_site.register(Group, GroupAdmin)


class TeamAdmin(admin.ModelAdmin):
    """Category Admin"""
    list_display = ["name", "size", "group"]
    fields = ["name", "size", "group"]

admin.site.register(Team, TeamAdmin)
challenge_designer_site.register(Team, TeamAdmin)
challenge_manager_site.register(Team, TeamAdmin)
developer_site.register(Team, TeamAdmin)


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
challenge_designer_site.register(Post, PostAdmin)
challenge_manager_site.register(Post, PostAdmin)
developer_site.register(Post, PostAdmin)

challenge_mgr.register_designer_challenge_info_model("Players", 2, Group, 2)
challenge_mgr.register_designer_challenge_info_model("Players", 2, Team, 2)
challenge_mgr.register_admin_challenge_info_model("Status", 1, Post, 5)
challenge_mgr.register_developer_challenge_info_model("Players", 2, Group, 1)
challenge_mgr.register_developer_challenge_info_model("Players", 2, Team, 2)
challenge_mgr.register_developer_challenge_info_model("Status", 4, Post, 5)
