'''
Forms for Prizes.
Created on Nov 4, 2012

@author: Cam Moore
'''

from django import forms
from apps.managers.challenge_mgr.models import RoundSetting


class ChangePrizeRoundForm(forms.Form):
    """change prize round form."""
    round_choice = forms.ModelChoiceField(queryset=RoundSetting.objects.all(), required=True)
