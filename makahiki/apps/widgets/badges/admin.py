"""Administrator interface to badge."""
from django.contrib import admin
from apps.managers.challenge_mgr import challenge_mgr
from apps.widgets.badges.models import Badge, BadgeAward


class BadgeAdmin(admin.ModelAdmin):
    """Category Admin"""
    list_display = ["name", "points", "award_condition", "award_trigger", "priority"]
    fields = ["name", "slug", "label", "description", "hint", "points", "priority",
              "award_condition", "award_trigger", "theme"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["priority"]

admin.site.register(Badge, BadgeAdmin)
admin.site.register(BadgeAward)
challenge_mgr.register_designer_game_info_model("Badge Game Mechanics", Badge)
challenge_mgr.register_admin_game_info_model("Badge Game Mechanics", BadgeAward)
challenge_mgr.register_developer_game_info_model("Badge Game Mechanics", Badge)
challenge_mgr.register_developer_game_info_model("Badge Game Mechanics", BadgeAward)
