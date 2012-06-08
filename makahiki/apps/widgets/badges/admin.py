"""Administrator interface to badge."""
from django.contrib import admin
from apps.widgets.badges.models import Badge


class BadgeAdmin(admin.ModelAdmin):
    """Category Admin"""
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Badge, BadgeAdmin)
