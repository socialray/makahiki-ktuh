"""Views handler for action_feedback rendering."""
from django.core.urlresolvers import reverse

import simplejson as json

from django.http import Http404, HttpResponse
from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings

from apps.widgets.action_feedback.forms import 

