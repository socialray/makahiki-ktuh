"""Views handler for ask admin page rendering."""
from django.core.urlresolvers import reverse

import simplejson as json

from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings

from apps.widgets.ask_admin.forms import FeedbackForm

ADMINS = (("Makahiki Developers", "makahiki-dev@googlegroups.com"),)
FROM_EMAIL = ADMINS[0][1]


def supply(request, page_name):
    """Supply view_objects for widget rendering, returns form."""
    _ = request
    _ = page_name
    form = FeedbackForm(auto_id="help_%s")
    form.url = reverse("help_index")
    return {
        "form": form,
        }


def send_feedback(request):
    """send feedback."""
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
            subject = u'[%s] %s asked a question' % (
                settings.CHALLENGE.competition_name,
                request.user.get_profile().name)

            if settings.CHALLENGE.email_enabled:
                mail = EmailMultiAlternatives(subject, message, FROM_EMAIL,
                    [settings.CHALLENGE.contact_email, ], headers={
                    "Reply-To": request.user.email})

                mail.attach_alternative(html_message, 'text/html')
                mail.send()

            #print "email sent %s" % html_message
            if request.is_ajax():
                return HttpResponse(json.dumps({"success": True}),
                                    mimetype="application/json")

    raise Http404
