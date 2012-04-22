"""Administrator interface to score_mgr."""
from django.contrib import admin

from apps.managers.score_mgr.models import ScoreSettings, ScoreboardEntry, PointsTransaction


admin.site.register(ScoreSettings)


class PointsTransactionAdmin(admin.ModelAdmin):
    """PointsTransaction administrator interface definition."""
    list_display = ["user", "transaction_date", "points", "message"]

admin.site.register(PointsTransaction, PointsTransactionAdmin)


class ScoreboardEntryAdmin(admin.ModelAdmin):
    """PointsTransaction administrator interface definition."""
    list_display = ["round_name", "profile", "points", "last_awarded_submission"]

admin.site.register(ScoreboardEntry, ScoreboardEntryAdmin)
