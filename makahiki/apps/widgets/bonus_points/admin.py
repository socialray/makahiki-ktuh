"""Admin definition for Bonus Points widget."""
'''
Created on Aug 5, 2012

@author: Cam Moore
'''

from django.contrib import admin
from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from apps.widgets.bonus_points.models import BonusPoint
from apps.managers.challenge_mgr import challenge_mgr


class BonusPointAdminForm(forms.ModelForm):
    """Bonus Points Admin Form."""
    point_value = forms.IntegerField(initial=5,
        label="Number of bonus points to award.",
        help_text="The number of bonus points the player earns.")

    class Meta:
        """Meta"""
        model = BonusPoint

    def save(self, *args, **kwargs):
        """Generates the number of bonus point codes."""
        _ = args
        _ = kwargs
        num = self.cleaned_data.get("num_codes")
        p = self.cleaned_data.get("point_value")
        # Generate
        if num > 0:
            BonusPoint.generate_bonus_points(p, num)


class BonusPointAdmin(admin.ModelAdmin):
    """admin for Bonus Points."""
    actions = ["delete_selected", "deactivate_selected"]
    list_display = ["code", "point_value", "is_active", "user"]

    form = BonusPointAdminForm

    def delete_selected(self, request, queryset):
        """override the delete selected method."""
        _ = request
        for obj in queryset:
            obj.delete()

    delete_selected.short_description = "Delete the selected Bonus Points."

    def deactivate_selected(self, request, queryset):
        """Changes the is_active flag to false for the selected Bonus Points."""
        _ = request
        queryset.update(is_active=False)

    deactivate_selected.short_description = "Deactivate the selected Bonus Points."

    def view_codes(self, request, queryset):
        """Views the Bonus Points Codes for printing."""
        _ = request
        _ = queryset
        response = HttpResponseRedirect(reverse("bonus_view_codes", args=()))
        return response


admin.site.register(BonusPoint, BonusPointAdmin)
challenge_mgr.register_game_admin_model("smartgrid", BonusPoint)
