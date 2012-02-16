"""
ask admin form
"""
from django import forms

class FeedbackForm(forms.Form):
    """feedback form"""
    url = forms.URLField(required=False, widget=forms.HiddenInput)
    question = forms.CharField(widget=forms.Textarea())
