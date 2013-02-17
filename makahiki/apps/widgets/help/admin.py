"""Provides the admin interface for help models."""

from django.contrib import admin
from django import forms
from apps.managers.challenge_mgr import challenge_mgr

from apps.widgets.help.models import HelpTopic
from apps.admin.admin import challenge_designer_site, challenge_manager_site, developer_site


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
    page_text = "Click on the slug to edit the details of the Help Topic. " + \
    "There are three categories of Help Topic, FAQs, Rules, and Widget. " + \
    "Widget Help Topics are displayed when a player clicks the help link for " + \
    "an individual widget. FAQs, and Rules are used by the Help FAQ widget and " + \
    "Help Rules widget."

    form = HelpAdminForm

admin.site.register(HelpTopic, HelpTopicAdmin)
challenge_designer_site.register(HelpTopic, HelpTopicAdmin)
challenge_manager_site.register(HelpTopic, HelpTopicAdmin)
developer_site.register(HelpTopic, HelpTopicAdmin)
challenge_mgr.register_designer_challenge_info_model("Other Settings", 3, HelpTopic, 2)
challenge_mgr.register_developer_challenge_info_model("Challenge", 1, HelpTopic, 5)
