#!/usr/bin/python

"""Invocation: compile_less.py [-v | --verbose]

Compiles all of the LESS style files into CSS.

Compiles all the themes and individual page style sheets, creating CSS files for each theme
containing all necessary definitions."""

import os
import glob
import getopt
import sys


def main(argv):
    """Compile Less main function. Usage: compile_less.py [-v | --verbose]"""
    verbose = 0
    try:
        opts, _ = getopt.getopt(argv, "v", ["verbose"])
    except getopt.GetoptError:
        print "Usage: compile_less.py [-v | --verbose]"
        sys.exit(2)

    for opt, _ in opts:
        if opt in ("-v", "--verbose"):
            verbose = 1

    page_names = ['landing',
                  'status',
                  'admin-base',
                  'admin']
    less_path = "static/less"
    os.chdir(less_path)
    theme_names = glob.glob('theme-*.less')
    for theme in theme_names:
        theme_name, _ = os.path.splitext(theme)
        if verbose == 1:
            print "Compiling %s.less" % theme_name
        os.system("lessc -x --yui-compress %s.less > ../css/%s.css" % (theme_name, theme_name))
    for page in page_names:
        if verbose == 1:
            print "Compiling %s.less" % page
        os.system("lessc -x --yui-compress %s.less > ../css/%s.css" % (page, page))

if __name__ == '__main__':
    main(sys.argv[1:])
