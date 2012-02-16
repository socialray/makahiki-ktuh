"""
main views module to render pages.
"""
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import importlib
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from django.conf import settings
import types

@never_cache
def root_index(request):
    """
    hanlde the landing page.
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse("home_index"))
    return HttpResponseRedirect(reverse("landing", args=()))


@never_cache
@login_required
def index(request):
    """
    handle dynamically lay-outed pages defined in page_settings.
    """
    page_name = request.path[1:][:-1]

    page_settings = settings.PAGE_SETTINGS[page_name]
    page_settings["PAGE_NAME"] = page_name

    view_objects = _get_view_objects(request, page_settings)

    page_layouts = {}
    page_layouts["DEFAULT"] = []
    responsive_css = ""

    for layout in page_settings["LAYOUTS"].items():
        responsive_css = _get_layout(page_layouts, layout, responsive_css)

    setting_objects = {
        "PAGE_NAME": page_settings["PAGE_NAME"],
        "PAGE_TITLE": page_settings["PAGE_TITLE"],
        "BASE_TEMPLATE": page_settings["BASE_TEMPLATE"],
        "CSS": page_settings["PAGE_NAME"],
        "RESPONSIVE_CSS": responsive_css,
        }

    return render_to_response("pages/templates/index.html", {
        "setting_objects": setting_objects,
        "view_objects": view_objects,
        "page_layouts": page_layouts,
        }, context_instance=RequestContext(request))

def _get_view_objects(request, page_settings):
    """ Returns view_objects supplied widgets defined in page_settings.py. """
    view_objects = {}
    default_layout = page_settings["LAYOUTS"]["DEFAULT"]
    for row in default_layout:
        for columns in row:
            if isinstance(columns, types.TupleType):
                gamelet = columns[0]
                view_module_name = 'apps.widgets.' + gamelet + '.views'
                page_views = importlib.import_module(view_module_name)
                view_objects[gamelet] = page_views.supply(request)
            else:
                gamelet = columns
                view_module_name = 'apps.widgets.' + gamelet + '.views'
                page_views = importlib.import_module(view_module_name)
                view_objects[gamelet] = page_views.supply(request)
                break
    
    return view_objects


def _create_responsive_css(row, idx, gid, percent, responsive_css):
    """Returns the responsive CSS."""
    if idx == 0:
        responsive_css += "#%s { float: left; width: %d%%; }" % (gid, percent)
    elif idx == len(row) - 1:
        if idx == 1: # second column of the two columns layout
            responsive_css += "#%s { float: right; width: %d%%; }" % (gid, percent)
        else:
            # last column of the three columns layout
            responsive_css += "#%s { float: left; width: %d%%; }" % (gid, percent)
    else:
        responsive_css += "#%s { float: right; width: %d%%; }" % (gid, percent)
    return responsive_css


def _get_layout(page_layouts, layout, responsive_css):
    """Returns the page_layouts definitions from page_settings.py."""
    if layout[0] == "PHONE_PORTRAIT":
        responsive_css += "\n@media screen and (max-width: 1000px) {\n"
    for row in layout[1]:
        column_layout = []
        for idx, columns in enumerate(row):
            if isinstance(columns, types.TupleType): # ((gamelet, 30%), (gamelet, 70%))
                gamelet = columns[0]
                gid = "%s" % (gamelet)
                percent = int(columns[1][:-1]) - 1
                gamelet_layout = {}
                responsive_css = _create_responsive_css(row, idx, gid, percent, responsive_css)
                if layout[0] == "DEFAULT":
                    gamelet_layout["id"] = gid
                    gamelet_layout["template"] = "widgets/%s/templates/index.html" % gamelet
                    column_layout += [gamelet_layout]
            else:  # (gamelet, 100%)
                gamelet = columns
                gid = gamelet
                percent = 100
                responsive_css += "#%s { float: none; width: %d%%; }" % (gid, percent)
                if layout[0] == "DEFAULT":
                    gamelet_layout = {}
                    gamelet_layout["id"] = gamelet
                    gamelet_layout["template"] = "widgets/%s/templates/index.html" % gamelet
                    column_layout += [gamelet_layout]
                    column_layout += [{}]
                
                break 
        
        if layout[0] == "DEFAULT":
            page_layouts["DEFAULT"] += [column_layout]
    
    if layout[0] == "PHONE_PORTRAIT":
        responsive_css += "\n}"
    return responsive_css