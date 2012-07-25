"""Admin method for logging in as another user."""
from django.conf import settings

from django.contrib.auth import SESSION_KEY
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from apps.managers.auth_mgr.forms import LoginForm


@user_passes_test(lambda u: u.is_staff, login_url="/account/cas/login")
def login_as(request, user_id):
    """Admin method for logging in as another user."""
    # ref: http://copiousfreetime.blogspot.com/2006/12/django-su.html
    user = get_object_or_404(User, id=user_id)
    if user.is_active:
        request.session[SESSION_KEY] = user_id
        request.session['staff'] = True
        # Expire this session when the browser closes.
        request.session.set_expiry(0)
    return HttpResponseRedirect(reverse("home_index"))


def login(request):
    """Show the login page and process the login form."""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.login(request):
            return HttpResponseRedirect(reverse("home_index"))
    else:
        form = LoginForm()

    return render_to_response("account/login.html", {"form": form},
                              context_instance=RequestContext(request))


def logout(request):
    """
    simply logout and redirect to landing page
    """
    username = request.user.username
    from django.contrib import auth

    # Sets a logout variable so that we can capture it in the logger.
    request.session["logged-out-user"] = username
    destination = "landing"

    auth.logout(request)

    if settings.CAS_SERVER_URL:
        return HttpResponseRedirect(reverse("cas_logout") + "?next=" + reverse(destination))
    else:
        return HttpResponseRedirect(reverse(destination))
