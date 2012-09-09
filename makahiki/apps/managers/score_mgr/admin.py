"""Administrator interface to score_mgr."""
from django.contrib import admin
from apps.managers.challenge_mgr import challenge_mgr

from apps.managers.score_mgr.models import ScoreSetting, ScoreboardEntry, PointsTransaction


class PointsTransactionAdmin(admin.ModelAdmin):
    """PointsTransaction administrator interface definition."""
    list_display = ["user", "transaction_date", "points", "message"]
    search_fields = ["user__username", "message"]
    list_filter = ['transaction_date']

admin.site.register(PointsTransaction, PointsTransactionAdmin)


class ScoreboardEntryAdmin(admin.ModelAdmin):
    """PointsTransaction administrator interface definition."""
    list_display = ["round_name", "profile", "points", "last_awarded_submission"]
    search_fields = ["profile__name", "profile__user__username"]

admin.site.register(ScoreboardEntry, ScoreboardEntryAdmin)


class ScoreSettingAdmin(admin.ModelAdmin):
    """PointsTransaction administrator interface definition."""
    list_display = ["setup_points", "referral_bonus_points", "active_threshold_points",
                    "signup_bonus_points", "noshow_penalty_points", "feedback_bonus_points", ]

admin.site.register(ScoreSetting, ScoreSettingAdmin)


challenge_mgr.register_site_admin_model("Challenge", ScoreSetting)
challenge_mgr.register_sys_admin_model("Status", PointsTransaction)
challenge_mgr.register_sys_admin_model("Status", ScoreboardEntry)
