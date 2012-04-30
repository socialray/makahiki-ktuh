"""post form"""

from django import forms


class WallForm(forms.Form):
    """Wall post form"""
    post = forms.CharField(widget=forms.widgets.Textarea())
    page_name = forms.CharField(widget=forms.HiddenInput(), required=False)
