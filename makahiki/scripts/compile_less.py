#!/usr/bin/python

"""Compiles the less styles into CSS.

Compiles all the themes and individual page style sheets."""

import os
import glob


def main():
    """main function."""

    page_names = ['advanced', 'energy', 'help', 'home', 'landing', 'learn',
                  'news', 'profile', 'status', 'win']
    less_path = "media/less"
    os.chdir(less_path)
    theme_names = glob.glob('theme-*.less')
    for theme in theme_names:
        (theme_name, theme_ext) = os.path.splitext(theme)
        os.system("lessc %s.less > ../css/%s.css" % (theme_name, theme_name))
    for page in page_names:
        os.system("lessc %s.less > ../css/%s.css" % (page, page))

if __name__ == '__main__':
    main()
