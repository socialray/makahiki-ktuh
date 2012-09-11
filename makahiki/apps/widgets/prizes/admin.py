"""Prize administrative interface."""
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.contrib import admin
from apps.managers.challenge_mgr import challenge_mgr
from apps.widgets.notifications.models import UserNotification, NoticeTemplate

from apps.widgets.prizes.models import Prize


class PrizeAdmin(admin.ModelAdmin):
    """raffle admin"""
    list_display = ('title', 'round_name', 'value', 'award_to', 'competition_type',
                    'winner', 'notice_sent')
    list_filter = ['round_name']
    actions = ["notify_winner"]

    def notify_winner(self, request, queryset):
        """pick winner."""
        _ = request
        for obj in queryset:
            leader = obj.leader()
            if leader and obj.award_to in ('individual_overall', 'individual_team')\
                and not self.notice_sent(obj):
                # Notify winner using the template.
                template = NoticeTemplate.objects.get(notice_type='prize-winner')
                message = template.render({'PRIZE': obj})
                UserNotification.create_info_notification(leader.user, message, True, obj)

                challenge = challenge_mgr.get_challenge()
                subject = "[%s] Congratulations, you won a prize!" % challenge.competition_name
                UserNotification.create_email_notification(
                    leader.user.email, subject, message, message)

        self.message_user(request, "Winners notification sent.")

    notify_winner.short_description = "Notify winner for selected prizes."

    def winner(self, obj):
        """return the winner and link to pickup form."""
        leader = obj.leader()
        if leader and obj.award_to in ('individual_overall', 'individual_team'):
            return "%s (<a href='%s'>View pickup form</a>)" % (leader,
            reverse('prize_view_form', args=(obj.pk,)))
        else:
            return leader
    winner.allow_tags = True
    winner.short_description = 'Winner'

    def notice_sent(self, obj):
        """return True if the notification had been sent."""
        leader = obj.leader()
        if leader and obj.award_to in ('individual_overall', 'individual_team'):
            return UserNotification.objects.filter(
                recipient=leader.user,
                content_type=ContentType.objects.get(model="prize"),
                object_id=obj.id).exists()
        else:
            return "N/A"
    notice_sent.short_description = 'Winner Notice Sent'


admin.site.register(Prize, PrizeAdmin)
challenge_mgr.register_game_admin_model("Top Score Game", Prize)
