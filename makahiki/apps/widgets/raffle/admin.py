"""Raffle widget administration"""

from django.contrib import admin
from django import forms
from django.core.urlresolvers import reverse

from apps.widgets.raffle.models import RafflePrize


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
    list_display = ('title', 'round_name', 'value')

admin.site.register(RafflePrize, RafflePrizeAdmin)
