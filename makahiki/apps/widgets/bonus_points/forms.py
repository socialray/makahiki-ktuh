"""Form for validating Bonus Points."""

'''
Created on Aug 5, 2012

@author: Cam Moore
'''

from django import forms


class BonusPointForm(forms.Form):
    """bonus points form in the Bonus Points widget."""
    response = forms.CharField(widget=forms.TextInput(attrs={'size': '12'}))


class GenerateBonusPointsForm(forms.Form):
    """Form for generating more bonus points codes."""
    point_value = forms.IntegerField(initial=5)
    num_codes = forms.IntegerField(initial=0)
