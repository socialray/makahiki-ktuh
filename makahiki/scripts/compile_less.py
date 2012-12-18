#!/usr/bin/python

"""Invocation: compile_less.py [-v | --verbose]

Compiles all of the LESS style files into CSS.

Compiles all the themes and individual page style sheets, creating CSS files for each theme
containing all necessary definitions."""

import os
import glob
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + os.sep + os.pardir + os.sep)
from apps.utils import script_utils


def main(argv):
    """Compile Less main function. Usage: compile_less.py [-v | --verbose]"""
    verbose = script_utils.has_verbose_flag(argv)
    page_names = ['landing',
                  'status',
                  'admin']
    less_path = script_utils.manage_py_dir() + "static/less"
    os.chdir(less_path)
    theme_names = glob.glob('theme-*.less')
    for theme in theme_names:
        theme_name, _ = os.path.splitext(theme)
        if verbose:
            print "Compiling %s.less" % theme_name
        os.system("lessc -x --yui-compress %s.less > ../css/%s.css" % (theme_name, theme_name))
    for page in page_names:
        if verbose:
            print "Compiling %s.less" % page
        os.system("lessc -x --yui-compress %s.less > ../css/%s.css" % (page, page))

if __name__ == '__main__':
    main(sys.argv[1:])
