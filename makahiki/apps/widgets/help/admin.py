"""Provides the admin interface for help models."""

from django.contrib import admin
from django import forms
from apps.managers.challenge_mgr import challenge_mgr

from apps.widgets.help.models import HelpTopic


class HelpAdminForm(forms.ModelForm):
    """The admin form for help topics."""
    class Meta:
        """meta"""
        model = HelpTopic

    def clean_parent_topic(self):
        """Prevents sub-topics of sub-topics.  Not possible with the current template layout."""

        parent_topic = self.cleaned_data["parent_topic"]
        if parent_topic and parent_topic.parent_topic:
            raise forms.ValidationError("This topic is also a sub-topic. "
                                        "Sub-topics of sub-topics are not "
                                        "allowed.")
        if parent_topic and parent_topic.slug == self.cleaned_data["slug"]:
            raise forms.ValidationError(
                "Topic cannot be a sub-topic of itself.")

        return parent_topic


class HelpTopicAdmin(admin.ModelAdmin):
    """Help topic administrative interface."""
    # Automatically populates the slug field.
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ["category", ]
    search_fields = ["slug", "title"]
    list_display = ["slug", "category", "priority", "parent_topic"]

    form = HelpAdminForm

admin.site.register(HelpTopic, HelpTopicAdmin)
challenge_mgr.register_designer_challenge_info_model("Other Settings", 3, HelpTopic, 2)
