from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import importlib
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

import settings
import types

@never_cache
def index(request):

  page_name = request.META["PATH_INFO"][1:]

  if page_name == '' or page_name == None:
      return HttpResponseRedirect(reverse("landing", args=()))

  page_module_name = 'pages.'+page_name+'.page_settings'
  page_settings = importlib.import_module(page_module_name)

  view_objects = {}
  default_layout = page_settings.LAYOUTS["DEFAULT"]
  for row in default_layout:
    for columns in row:
      if isinstance(columns, types.TupleType):
          gamelet = columns[0]
      else:
          gamelet = columns
          break

      view_module_name = 'apps.gamelets.'+gamelet+'.views'
      page_views = importlib.import_module(view_module_name)
      view_objects[gamelet] = page_views.supply(request)

  setting_objects = {
      "PAGE_TITLE" : page_settings.PAGE_TITLE,
      "BASE_TEMPLATE" : page_settings.BASE_TEMPLATE,
      "CSS" : page_settings.CSS,
  }

  return render_to_response("pages/"+page_name+"/templates/index.html", {
      "setting_objects" : setting_objects,
      "view_objects" : view_objects,
      }, context_instance=RequestContext(request))
