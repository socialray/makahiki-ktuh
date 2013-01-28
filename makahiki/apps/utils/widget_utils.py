"""Utility modules for widget creation."""

import shutil
from django.conf import settings
import os


def create_widget(name):
    """create the widget directory structure."""

    template_dir = settings.PROJECT_ROOT + "/apps/utils/widget_templates"
    widget_dir = settings.PROJECT_ROOT + "/apps/widgets/" + name

    if os.path.exists(widget_dir):
        print "A directory with the same name already exists in the widgets directory"
        return

    # create widget directory structure
    shutil.copytree(template_dir, widget_dir)
    print "created widget directory stucture under " + widget_dir
