"""Administrator interface to badge."""
from django.contrib import admin
from apps.managers.challenge_mgr import challenge_mgr
from apps.widgets.badges.models import Badge, BadgeAward
from apps.admin.admin import challenge_designer_site, challenge_manager_site, developer_site


class BadgeAdmin(admin.ModelAdmin):
    """Category Admin"""
    list_display = ["name", "points", "award_condition", "award_trigger", "priority"]
    fields = ["name", "slug", "label", "description", "hint", "points", "priority",
              "award_condition", "award_trigger", "theme"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["priority"]

admin.site.register(Badge, BadgeAdmin)
challenge_designer_site.register(Badge, BadgeAdmin)
challenge_manager_site.register(Badge, BadgeAdmin)
developer_site.register(Badge, BadgeAdmin)
admin.site.register(BadgeAward)
challenge_designer_site.register(BadgeAward)
challenge_manager_site.register(BadgeAward)
developer_site.register(BadgeAward)
challenge_mgr.register_designer_game_info_model("Badge Game Mechanics", Badge)
challenge_mgr.register_admin_game_info_model("Badge Game Mechanics", BadgeAward)
challenge_mgr.register_developer_game_info_model("Badge Game Mechanics", Badge)
challenge_mgr.register_developer_game_info_model("Badge Game Mechanics", BadgeAward)
