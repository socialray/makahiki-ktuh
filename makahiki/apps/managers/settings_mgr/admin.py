"""
settings manager Admin
"""
from django.contrib import admin
from apps.managers.settings_mgr.models import ChallengeSettings, RoundSettings, PageSettings

admin.site.register(ChallengeSettings)
admin.site.register(RoundSettings)
admin.site.register(PageSettings)
