"""Raffle widget administration"""

from django.contrib import admin
from django import forms
from django.core.urlresolvers import reverse
from apps.managers.challenge_mgr import challenge_mgr

from apps.widgets.raffle.models import RafflePrize, RaffleTicket


class RafflePrizeAdminForm(forms.ModelForm):
    """raffle admin form"""
    class Meta:
        """meta"""
        model = RafflePrize

    def __init__(self, *args, **kwargs):
        """Override to have a link to winner of the prize."""
        super(RafflePrizeAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.winner:
            self.fields['winner'].help_text = 'View pickup <a href="%s">form</a>' % reverse(
                'raffle_view_form', args=(self.instance.id,))
        else:
            self.fields['winner'].help_text = ''


class RafflePrizeAdmin(admin.ModelAdmin):
    """raffle admin"""
    form = RafflePrizeAdminForm
    list_display = ('title', 'round_name', 'value', 'winner_form')

    def winner_form(self, obj):
        """return the winner and link to pickup form."""
        if obj.winner:
            return "%s (<a href='%s'>View pickup form</a>)" % (obj.winner,
            reverse('raffle_view_form', args=(obj.pk,)))
        else:
            return '(None)'
    winner_form.allow_tags = True
    winner_form.short_description = 'Winner'

admin.site.register(RafflePrize, RafflePrizeAdmin)
challenge_mgr.register_game_admin_model("raffle", RafflePrize)


class RaffleTicketAdmin(admin.ModelAdmin):
    """raffle ticket admin"""
    list_display = ('raffle_prize', 'user')

admin.site.register(RaffleTicket, RaffleTicketAdmin)
challenge_mgr.register_game_admin_model("raffle", RaffleTicket)
