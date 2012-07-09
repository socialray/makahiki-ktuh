"""Prize administrative interface."""
from django.core.urlresolvers import reverse
from django.contrib import admin
from apps.managers.challenge_mgr import challenge_mgr

from apps.widgets.prizes.models import Prize


class PrizeAdmin(admin.ModelAdmin):
    """raffle admin"""
    list_display = ('title', 'round_name', 'value', 'award_to', 'winner')

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


admin.site.register(Prize, PrizeAdmin)
challenge_mgr.register_game_admin_model("prizes", Prize)
