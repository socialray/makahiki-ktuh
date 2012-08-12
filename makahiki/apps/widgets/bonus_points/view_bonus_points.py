'''
Created on Aug 4, 2012

@author: Cam Moore
'''
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.http import Http404
from apps.widgets.bonus_points.models import BonusPoint
from django.shortcuts import render_to_response
from django.template.context import RequestContext


@never_cache
@login_required
def view_codes(request):
    """View the bonus points codes."""
    if not request.user or not request.user.is_staff:
        raise Http404

    per_page = 10
    # Check for a rows parameter
    if "rows" in request.GET:
        per_page = int(request.GET['rows'])

    codes = BonusPoint.objects.order_by('pk')
    if len(codes) == 0:
        raise Http404

    return render_to_response("view_bonus_points.html", {
        "codes": codes,
        "per_page": per_page,
        }, context_instance=RequestContext(request))
