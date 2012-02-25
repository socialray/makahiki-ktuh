"""
views handler for ask admin page rendering.
"""
import simplejson as json

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
from django.contrib.sites.models import Site
from django.conf import settings

from widgets.ask_admin.forms import FeedbackForm

FROM_EMAIL = settings.MANAGERS[0][1]

def supply(request, page_name):
    """ supply view_objects for widget rendering."""
    _ = request
    _ = page_name
    form = FeedbackForm(auto_id="help_%s")
    return {
        "form": form,
        }

def send_feedback(request):
    """send feedbacl"""
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            html_message = render_to_string("email/ask_admin.html", {
                "user": request.user,
                "url": form.cleaned_data["url"],
                "question": form.cleaned_data["question"],
                })
            message = render_to_string("email/ask_admin.txt", {
                "user": request.user,
                "url": form.cleaned_data["url"],
                "question": form.cleaned_data["question"],
                })

            # Using adapted version from Django source code
            current_site = Site.objects.get(id=settings.SITE_ID)
            subject = u'[%s] %s asked a question' % (
            current_site.domain, request.user.get_profile().name)
            mail = EmailMultiAlternatives(subject, message, FROM_EMAIL,
                [settings.CONTACT_EMAIL, ], headers={"Reply-To": request.user.email})

            mail.attach_alternative(html_message, 'text/html')
            mail.send()

            if request.is_ajax():
                return HttpResponse(json.dumps({"success": True}), mimetype="application/json")

            return HttpResponseRedirect(form.cleaned_data["url"])

    raise Http404