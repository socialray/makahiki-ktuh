"""Administrator interface to score_mgr."""
from django.contrib import admin
from apps.managers.challenge_mgr import challenge_mgr

from apps.managers.score_mgr.models import ScoreSetting, ScoreboardEntry, PointsTransaction


admin.site.register(ScoreSetting)


class PointsTransactionAdmin(admin.ModelAdmin):
    """PointsTransaction administrator interface definition."""
    list_display = ["user", "transaction_date", "points", "message"]

admin.site.register(PointsTransaction, PointsTransactionAdmin)


class ScoreboardEntryAdmin(admin.ModelAdmin):
    """PointsTransaction administrator interface definition."""
    list_display = ["round_name", "profile", "points", "last_awarded_submission"]

admin.site.register(ScoreboardEntry, ScoreboardEntryAdmin)

challenge_mgr.register_site_admin_model("Challenge", ScoreSetting)
challenge_mgr.register_sys_admin_model("Logs", PointsTransaction)
challenge_mgr.register_sys_admin_model("Logs", ScoreboardEntry)
