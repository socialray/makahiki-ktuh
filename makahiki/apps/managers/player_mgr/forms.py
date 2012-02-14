from django import forms

from managers.player_mgr.models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'points', 'floor', 'first_name', 'last_name')
