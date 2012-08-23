"""Handle player admin."""

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from apps.managers.player_mgr.player_mgr import bulk_create_players


def bulk_upload_form(request):
    """prompt for the bulk user upload form."""
    return render_to_response("admin/auth/user/bulk_upload_form.html", {},
            context_instance=RequestContext(request))


def bulk_create(request):
    """bulk create the users from the upload."""
    if request.method == "POST":
        if 'csvfile' in request.FILES:
            total_load = bulk_create_players(request.FILES['csvfile'])
            messages.success(request, "Total user created: %d" % total_load)
            return HttpResponseRedirect("/admin/auth/user/")
