"""Provides the view of the My_Info widget, which both displays profile info and allows updates."""

from apps.widgets.my_info.forms import ProfileForm


def supply(request, page_name):
    """Supply view_objects for My_Info and process the POST command."""
    _ = page_name
    user = request.user
    form = None
    if request.method == "POST":
        user = request.user
        form = ProfileForm(request.POST, user=request.user)
        if form.is_valid():
            profile = user.get_profile()
            name = form.cleaned_data["display_name"].strip()

            if name != profile.name:
                profile.name = name

            profile.contact_email = form.cleaned_data["contact_email"]
            profile.contact_text = form.cleaned_data["contact_text"]
            profile.contact_carrier = form.cleaned_data["contact_carrier"]
            # profile.enable_help = form.cleaned_data["enable_help"]

            profile.save()
            form.message = "Your changes have been saved"

        else:
            form.message = "Please correct the errors below."

    # If this is a new request, initialize the form.
    if not form:
        profile = user.get_profile()
        form = ProfileForm(initial={
            # "enable_help": user.get_profile().enable_help,
            "display_name": profile.name,
            "contact_email": profile.contact_email or user.email,
            "contact_text": profile.contact_text,
            "contact_carrier": profile.contact_carrier,
            })

        if "changed_avatar" in request.GET:
            form.message = "Your avatar has been updated."

    return {
        "form": form,
    }
