'''
Created on Apr 16, 2013

@author: shindig
'''
from django import forms

class ProjectForm(forms.Form):
    title = forms.CharField(max_length=75)
    short_description = forms.CharField(max_length=300)
    long_description = forms.CharField(widget=forms.Textarea)
    max_number_of_members = forms.IntegerField(max_value=6, min_value=1)