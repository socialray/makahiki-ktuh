"""Provides the view of the My_Info widget, which both displays profile info and allows updates."""
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from apps.managers.cache_mgr import cache_mgr
from apps.managers.challenge_mgr import challenge_mgr
from apps.widgets.my_info.forms import ProfileForm


def supply(request, page_name):
    """Supply view_objects for My_Info and process the POST command."""
    _ = page_name

    session = request.session
    form = None
    if "form" in session:
        form = session.pop('form')

    if not form:
        user = request.user
        profile = user.get_profile()
        user_theme = profile.theme
        if not user_theme:
            user_theme = challenge_mgr.get_challenge().theme
        form = ProfileForm(initial={
            "display_name": profile.name,
            "contact_email": user.email,
            "contact_text": profile.contact_text,
            "contact_carrier": profile.contact_carrier,
            "theme": user_theme,
            })

        if "changed_avatar" in request.GET:
            form.message = "Your avatar has been updated."

    return {
        "form": form,
    }


def save(request):
    """profile save"""
    form = None
    if request.method == "POST":
        user = request.user
        form = ProfileForm(request.POST, user=request.user.username)
        if form.is_valid():
            profile = user.get_profile()
            name = form.cleaned_data["display_name"].strip()

            if name != profile.name:
                profile.name = name

            user.email = form.cleaned_data["contact_email"]
            user.save()
            profile.contact_text = form.cleaned_data["contact_text"]
            profile.contact_carrier = form.cleaned_data["contact_carrier"]

            theme = form.cleaned_data["theme"].strip()
            if theme and theme != profile.theme:
                profile.theme = theme
                # Invalidate quest bar cache.
                cache_mgr.delete('get_quests-%s' % user.username)

            profile.save()

            # Invalidate info bar cache.
            cache_mgr.invalidate_template_cache("RIB", user.username)

            form.message = "Your changes have been saved"
        else:
            form.message = "Please correct the errors below."

        request.session['form'] = form

    return HttpResponseRedirect(reverse("profile_index", args=()))
