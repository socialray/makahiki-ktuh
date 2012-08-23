"""
main views module to render pages.
"""
import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import importlib
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.managers.cache_mgr import cache_mgr
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.resource_mgr import resource_mgr


@never_cache
def root_index(request):
    """
    handle the landing page.
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse("home_index"))
    return HttpResponseRedirect(reverse("landing", args=()))


@never_cache
@login_required
def index(request):
    """
    handle top level pages.
    """
    page_name = request.path[1:][:-1]

    view_objects = {}

    page_info = challenge_mgr.page_info(request.user, page_name)
    if not page_info:
        raise Http404
    elif not page_info.is_unlock:
        return HttpResponseForbidden('<h1>Permission denied</h1>')

    # get the view_objects
    is_page_defined = supply_view_objects(request, page_name, view_objects)

    if not is_page_defined:
        raise Http404

    # get user resource rank and usage
    team = request.user.get_profile().team
    if team:
        energy_page = challenge_mgr.page_info(request.user, "energy")
        water_page = challenge_mgr.page_info(request.user, "water")
        if energy_page and energy_page.is_unlock:
            view_objects["energy_rank_info"] = resource_mgr.resource_team_rank_info(team, "energy")
        if water_page and water_page.is_unlock:
            view_objects["water_rank_info"] = resource_mgr.resource_team_rank_info(team, "water")

    time_start = datetime.datetime.now()
    response = render_to_response("%s.html" % page_name, {
        "view_objects": view_objects,
        }, context_instance=RequestContext(request))
    time_end = datetime.datetime.now()
    print "%s time: %s" % ("render", (time_end - time_start))

    return response


def supply_view_objects(request, page_name, view_objects):
    """ Returns view_objects supplied widgets defined in PageSetting. """

    widgets = challenge_mgr.get_enabled_widgets(page_name)
    if not widgets:
        return False

    view_objects['widget_templates'] = []
    for widget in widgets:
        view_module_name = 'apps.widgets.' + widget + '.views'
        page_views = importlib.import_module(view_module_name)
        widget = widget.replace(".", "__")

        time_start = datetime.datetime.now()
        view_objects[widget] = page_views.supply(request, page_name)
        time_end = datetime.datetime.now()
        print "%s time: %s" % (view_module_name, (time_end - time_start))

        widget_template = "widgets/" + widget.replace(".", "/") + "/templates/index.html"
        view_objects['widget_templates'].append(widget_template)

    return True


@user_passes_test(lambda u: u.is_staff, login_url="/landing")
def clear_cache(request):
    """clear all cached content."""
    _ = request
    cache_mgr.clear()
    return HttpResponseRedirect("/admin")
