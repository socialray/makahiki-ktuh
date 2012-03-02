"""Prize admin"""
from django.contrib import admin

from apps.widgets.prizes.models import Prize

admin.site.register(Prize)
