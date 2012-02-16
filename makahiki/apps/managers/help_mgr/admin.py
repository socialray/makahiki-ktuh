"""
admin for help widget models
"""
from django.contrib import admin
from django import forms

from managers.help_mgr.models import HelpTopic

class HelpAdminForm(forms.ModelForm):
    """admin form"""
    class Meta:
        """meta"""
        model = HelpTopic

    def clean_parent_topic(self):
        """
        Prevents sub-topics of sub-topics.  It cannot be done with the current template layout.
        """
        parent_topic = self.cleaned_data["parent_topic"]
        if parent_topic and parent_topic.parent_topic:
            raise forms.ValidationError(
                "This topic is also a sub-topic. Sub-topics of sub-topics are not allowed.")
        if parent_topic and parent_topic.slug == self.cleaned_data["slug"]:
            raise forms.ValidationError(
                "Topic cannot be a sub-topic of itself.")

        return parent_topic


class HelpTopicAdmin(admin.ModelAdmin):
    """help topic admin"""
    # Automatically populates the slug field.
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ["category", ]

    form = HelpAdminForm

admin.site.register(HelpTopic, HelpTopicAdmin)