"""Quest administrative interface, enabling checking of quest conditions."""

from django.contrib import admin
from django import forms
from apps.managers.challenge_mgr import challenge_mgr
from apps.utils import utils

from apps.widgets.quests.models import Quest
from apps.admin.admin import challenge_designer_site, challenge_manager_site, developer_site


class QuestAdminForm(forms.ModelForm):
    """admin form"""
    class Meta:
        """meta"""
        model = Quest

    def clean_unlock_conditions(self):
        """Validates the unlock conditions of the quest."""
        data = self.cleaned_data["unlock_conditions"]
        utils.validate_form_predicates(data)
        return data

    def clean_completion_conditions(self):
        """Validates the unlock conditions of the quest."""
        data = self.cleaned_data["completion_conditions"]
        utils.validate_form_predicates(data)
        return data


class QuestAdmin(admin.ModelAdmin):
    """Admin"""
    list_display = ["name", "priority", "unlock_conditions"]
    ordering = ["priority"]

    # Automatically populates the slug field.
    prepopulated_fields = {"quest_slug": ("name",)}

    form = QuestAdminForm

admin.site.register(Quest, QuestAdmin)
challenge_designer_site.register(Quest, QuestAdmin)
challenge_manager_site.register(Quest, QuestAdmin)
developer_site.register(Quest, QuestAdmin)
challenge_mgr.register_designer_game_info_model("Quest Game Mechanics", Quest)
challenge_mgr.register_developer_game_info_model("Quest Game Mechanics", Quest)
