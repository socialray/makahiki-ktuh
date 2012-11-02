'''
Forms for Raffle Prizes.
Created on Nov 1, 2012

@author: Cam Moore
'''

from django import forms
from apps.managers.challenge_mgr.models import RoundSetting


class ChangeRoundForm(forms.Form):
    """change round form."""
    round_choice = forms.ModelChoiceField(queryset=RoundSetting.objects.all(), required=True)
