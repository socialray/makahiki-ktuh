"""Administrator interface to score_mgr."""
from django.contrib import admin

from apps.managers.score_mgr.models import ScoreSettings


admin.site.register(ScoreSettings)
