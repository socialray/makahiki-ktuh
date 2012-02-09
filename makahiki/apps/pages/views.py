from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import importlib
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

import settings
import types

@never_cache
def root_index(request):
  if request.user.is_authenticated():
    return HttpResponseRedirect(reverse("home_index"))
  return HttpResponseRedirect(reverse("landing", args=()))

@never_cache
@login_required
def index(request):
  page_name = request.path[1:][:-1]

  page_settings = settings.PAGE_SETTINGS[page_name]
  page_settings["PAGE_NAME"] = page_name

  view_objects = {}
  default_layout = page_settings["LAYOUTS"]["DEFAULT"]
  for row in default_layout:
    for columns in row:
      if isinstance(columns, types.TupleType):
          gamelet = columns[0]
          view_module_name = 'apps.widgets.'+gamelet+'.views'
          page_views = importlib.import_module(view_module_name)
          view_objects[gamelet] = page_views.supply(request)
      else:
          gamelet = columns
          view_module_name = 'apps.widgets.'+gamelet+'.views'
          page_views = importlib.import_module(view_module_name)
          view_objects[gamelet] = page_views.supply(request)
          break

  page_layouts = {}
  page_layouts["DEFAULT"] = []
  responsive_css = ""

  for layout in page_settings["LAYOUTS"].items():
    if layout[0] == "PHONE_PORTRAIT":
        responsive_css += "\n@media screen and (max-width: 1000px) {\n"

    for row in layout[1]:
        column_layout = []
        for idx, columns in enumerate(row):
          if isinstance(columns, types.TupleType):   # ((gamelet, 30%), (gamelet, 70%))
              gamelet = columns[0]
              id = "%s" % (gamelet)
              percent = int(columns[1][:-1]) - 1
              gamelet_layout = {}
              if idx == 0:
                  responsive_css += "#%s { float: left; width: %d%%; }" % (id, percent)
              elif idx == len(row)-1:
                  if idx == 1:        # second column of the two columns layout
                      responsive_css += "#%s { float: right; width: %d%%; }" % (id, percent)
                  else:               # last column of the three columns layout
                      responsive_css += "#%s { float: left; width: %d%%; }" % (id, percent)
              else:
                  responsive_css += "#%s { float: right; width: %d%%; }" % (id, percent)

              if layout[0] == "DEFAULT":
                gamelet_layout["id"] = id
                gamelet_layout["template"] = "widgets/%s/templates/index.html" % gamelet
                column_layout += [gamelet_layout]
          else:                                      # (gamelet, 100%)
              gamelet = columns
              id = gamelet
              percent = 100
              responsive_css += "#%s { float: none; width: %d%%; }" % (id, percent)

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

  setting_objects = {
      "PAGE_NAME" : page_settings["PAGE_NAME"],
      "PAGE_TITLE" : page_settings["PAGE_TITLE"],
      "BASE_TEMPLATE" : page_settings["BASE_TEMPLATE"],
      "CSS" : page_settings["PAGE_NAME"],
      "RESPONSIVE_CSS" : responsive_css,
      }

  return render_to_response("pages/templates/index.html", {
      "setting_objects" : setting_objects,
      "view_objects" : view_objects,
      "page_layouts": page_layouts,
      }, context_instance=RequestContext(request))
