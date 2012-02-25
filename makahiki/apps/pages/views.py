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

    if not page_name in settings.PAGE_SETTINGS.keys():
        return HttpResponseRedirect(reverse("home_index"))

    page_settings = settings.PAGE_SETTINGS[page_name]
    page_settings["PAGE_NAME"] = page_name

    # get the view_objects
    view_objects = _get_view_objects(request, page_settings)

    # get the page layout and responsive style
    page_layouts = {}
    page_layouts["DEFAULT"] = []
    extra_css = ""
    for layout in page_settings["LAYOUTS"].items():
        extra_css = _get_layout(page_layouts, layout, extra_css)

    # get tbe page and widget css
    extra_css  += _get_widget_css(view_objects)

    setting_objects = {
        "PAGE_NAME": page_settings["PAGE_NAME"],
        "PAGE_TITLE": page_settings["PAGE_TITLE"],
        "BASE_TEMPLATE": page_settings["BASE_TEMPLATE"],
        "PAGE_CSS": page_name,
        "EXTRA_CSS": extra_css,
        }

    # get user energy rank and usage
    energy_rank_info = None
    if "widgets.energy_scoreboard" in settings.INSTALLED_WIDGET_APPS:
        module = importlib.import_module("apps.widgets.energy_scoreboard.models")
        energy_rank_info = module.EnergyData.get_team_overall_rank_info(
            request.user.get_profile().team)

    return render_to_response("pages/templates/index.html", {
        "setting_objects": setting_objects,
        "view_objects": view_objects,
        "page_layouts": page_layouts,
        "energy_rank_info": energy_rank_info,
        }, context_instance=RequestContext(request))



def _get_view_objects(request, page_settings):
    """ Returns view_objects supplied widgets defined in page_settings.py. """
    view_objects = {}
    default_layout = page_settings["LAYOUTS"]["DEFAULT"]
    page_name = page_settings["PAGE_NAME"]
    for row in default_layout:
        for columns in row:
            if isinstance(columns, types.TupleType):
                widget = columns[0]
                _load_widget_module(request, widget, view_objects, page_name)
            else:
                widget = columns
                _load_widget_module(request, widget, view_objects, page_name)
                break
    
    return view_objects

def _load_widget_module(request, widget, view_objects, page_name):
    """Loads the widget modules"""
    view_module_name = 'apps.widgets.' + widget + '.views'
    page_views = importlib.import_module(view_module_name)
    view_objects[widget] = page_views.supply(request, page_name)

def _get_widget_css(view_objects):
    """
    Returns the contents of the available widget css file
    """
    widget_css = ""
    for widget in view_objects.keys():
        widget_css_file = "%s/apps/widgets/%s/templates/css.css" % (settings.PROJECT_ROOT, widget)
        try:
            infile = open(widget_css_file)
            widget_css += infile.read() + "\n"
        except IOError:
            pass
    return widget_css

def _get_layout(page_layouts, layout, css_style):
    """Fills in the page_layouts definitions from page_settings.py, Returns css style"""

    if layout[0] == "PHONE_PORTRAIT":
        css_style += "\n@media screen and (max-width: 1000px) {\n"  # responsive style
    layout_style = ""
    for row in layout[1]:
        column_layout = []
        percent_total = 0
        for columns in row:
            if isinstance(columns, types.TupleType): # ((widget, 30%), (widget, 70%))
                widget = columns[0]
                gid = "%s" % (widget)

                percent = int(columns[1][:-1]) - 1
                percent_total += percent
                if percent_total < 95:
                    layout_style += "#%s { float: left; width: %d%%; }" % (gid, percent)
                else:
                    layout_style += "#%s { float: right; width: %d%%; }" % (gid, percent)
                    percent_total = 0

                widget_layout = {}
                if layout[0] == "DEFAULT":
                    widget_layout["id"] = gid
                    widget_layout["template"] = "widgets/%s/templates/index.html" % widget
                    column_layout += [widget_layout]
            else:  # (widget, 100%)
                widget = columns
                gid = widget

                percent = 100
                layout_style += "#%s { float: left; width: %d%%; }" % (gid, percent)
                if layout[0] == "DEFAULT":
                    widget_layout = {}
                    widget_layout["id"] = widget
                    widget_layout["template"] = "widgets/%s/templates/index.html" % widget
                    column_layout += [widget_layout]
                    column_layout += [{}]
                
                break 
        
        if layout[0] == "DEFAULT":
            page_layouts["DEFAULT"] += [column_layout]

    css_style += layout_style

    if layout[0] == "PHONE_PORTRAIT":
        css_style += "\n}"
    return css_style