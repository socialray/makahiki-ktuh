"""Administrator interface to badge."""
from django.contrib import admin
from apps.managers.challenge_mgr import challenge_mgr
from apps.widgets.badges.models import Badge


class BadgeAdmin(admin.ModelAdmin):
    """Category Admin"""
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Badge, BadgeAdmin)
challenge_mgr.register_game_admin_model("badges", Badge)
