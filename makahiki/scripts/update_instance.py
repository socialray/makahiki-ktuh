#!/usr/bin/python

"""
Invocation:  scripts/update_instance .py -r|--heroku[=] <heroku_app>

Use this script to update an instance:

if -r or --heroku is specified, it will initialize the instance in the specified
heroku app.

Performs the following:
  * Updates and/or installation of any modules in requirements.txt
  * Synchronize and migrates the database schemas.
  * Collects and copies the static and media files to the specific location.
"""

import getopt
import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + os.sep + os.pardir + os.sep)
from apps.utils import script_utils


def main(argv):
    """main function."""
    heroku_app = None
    manage_py = script_utils.manage_py_command()
    manage_command = "python " + manage_py

    try:
        opts, args = getopt.getopt(argv, "r:h", ["heroku=", "help"])
    except getopt.GetoptError:
        script_utils.exit_with_help(__doc__)

    for opt in opts:
        if opt[0] == "-h" or opt[0] == "--help":
            script_utils.exit_with_help(__doc__)
        if opt[0] == "-r" or opt[0] == "--heroku":
            heroku_app = opt[1]
            manage_command = "heroku run --app %s python makahiki/manage.py" % heroku_app

    _ = args

    if not heroku_app:
        script_utils.install_requirements()
    else:
        script_utils.push_to_heroku(heroku_app)

    script_utils.syncdb(manage_command)

    script_utils.copy_static_media(heroku_app)


if __name__ == '__main__':
    main(sys.argv[1:])
