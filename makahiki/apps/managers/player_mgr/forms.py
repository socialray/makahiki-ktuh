from django import forms

from managers.player_mgr.models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'points', 'team', 'first_name', 'last_name')
