#!/usr/bin/python

"""Compiles the less styles into CSS.

Compiles all the themes and individual page style sheets."""

import os


def main():
    """main function."""

    theme_names = ['theme', 'default']
    page_names = ['advanced', 'energy', 'help', 'home', 'landing', 'learn',
                  'news', 'profile', 'status', 'win']
    media_dir = "media"
    less_path = os.path.join(media_dir, "less")
    os.chdir(less_path)
    for theme in theme_names:
        os.system("lessc %s.less > ../css/%s.css" % (theme, theme))
        os.system("lessc %s-advanced.less > ../css/%s-advanced.css" % (theme, theme))
    for page in page_names:
        os.system("lessc %s.less > ../css/%s.css" % (page, page))

if __name__ == '__main__':
    main()
