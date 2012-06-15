"""Forms for action_feedback."""

from django import forms


class ActionFeedbackForm(forms.Form):
    """Action Feedback form"""
    comments = forms.CharField(widget=forms.widgets.Textarea())
    score = forms.IntegerField(widget=forms.widgets.RadioSelect())
