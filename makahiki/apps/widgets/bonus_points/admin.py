"""Admin definition for Bonus Points widget."""
from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.admin.admin import challenge_designer_site, challenge_manager_site, developer_site


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
    actions = ["delete_selected", "deactivate_selected", "view_selected",
               "print_selected"]
    list_display = ["pk", "code", "point_value", "create_date", "is_active",
                    "printed_or_distributed", "user"]
    ordering = ["-create_date", "is_active"]
    list_filter = ["point_value", "is_active", "printed_or_distributed"]
    date_hierarchy = "create_date"

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

    def print_selected(self, request, queryset):
        """Changes the printed_or_distributed flag to True for the selected
        Bonus Points."""
        _ = request
        queryset.update(printed_or_distributed=True)

    print_selected.short_description = "Set the printed or distributed flag."

    def view_selected(self, request, queryset):
        """Views the Bonus Points Codes for printing."""
        _ = request
        _ = queryset

        return render_to_response("view_bonus_points.html", {
            "codes": queryset,
            "per_page": 10,
        }, context_instance=RequestContext(request))

    view_selected.short_description = "View the selected Bonus Points."

    def view_codes(self, request, queryset):
        """Views the Bonus Points Codes for printing."""
        _ = request
        _ = queryset

        response = HttpResponseRedirect(reverse("bonus_view_codes", args=()))
        return response


admin.site.register(BonusPoint, BonusPointAdmin)
challenge_designer_site.register(BonusPoint, BonusPointAdmin)
challenge_manager_site.register(BonusPoint, BonusPointAdmin)
developer_site.register(BonusPoint, BonusPointAdmin)
challenge_mgr.register_designer_game_info_model("Smart Grid Game", BonusPoint)
challenge_mgr.register_admin_game_info_model("Smart Grid Game", BonusPoint)
challenge_mgr.register_developer_game_info_model("Smart Grid Game", BonusPoint)
