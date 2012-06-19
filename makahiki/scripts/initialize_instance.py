#!/usr/bin/python

"""
Invocation:  scripts/initialize_instance .py -t|--type[=] default|demo|test
                                             -r|--heroku[=] <heroku_app>

Use this script to create an instance with different types of configuration:

[default]: includes the basic configuration. The admin needs to create
           the settings for rounds, resources, resource goals, teams and
           users, prizes, etc. Uses internal authentication.

[demo]   : includes all of the [default] configuration, with the additions of
           demo data, such as demo rounds, resource and goal settings, demo
           team, demo users, demo prizes. Uses internal authentication.

[test]   : includes all of "demo" configuration, with more test users. Uses
           CAS authentication.

if -r or --heroku is specified, it will initialize the instance in the specified
heroku app.

Performs the following:
  * Updates and/or installation of any modules in requirements.txt
  * Syncs the database and migrates the database schemas.
  * Collects and copies the static and media files to the desired location.
  * Loads the default or test configuration of data.
"""

import getopt

import os
import sys


def exit_with_help():
    """Print usage of the command, then exit with error code."""
    print __doc__
    sys.exit(2)


def copy_static_media(manage_command, heroku_app):
    """copy static media."""
    print "collecting static and media files..."
    os.system("%s collectstatic --noinput --verbosity 0" % manage_command)

    if not heroku_app:
        os.system("cp -r media site_media")
    else:
        # always use S3 in heorku, need to upload the media directory to S3 bucket
        command = "s3put -a %s -s %s -b %s -p `pwd` %s" % (
            os.environ['MAKAHIKI_AWS_ACCESS_KEY_ID'],
            os.environ['MAKAHIKI_AWS_SECRET_ACCESS_KEY'],
            os.environ['MAKAHIKI_AWS_STORAGE_BUCKET_NAME'],
            "media"
            )
        print command
        #os.system(command)


def reset_db(heroku_app):
    """reset db."""
    print "resetting the db..."
    if not heroku_app:
        os.system("python scripts/initialize_postgres.py")
    else:
        os.system("heroku pg:reset SHARED_DATABASE --app %s  --confirm %s" % (
            heroku_app, heroku_app))


def install_requirements(heroku_app):
    """install requirements."""
    if not heroku_app:
        print "installing requirements..."
        os.system("pip install -r ../requirements.txt --quiet")


def load_fixtures(manage_command, fixture_path, prefix):
    """load fixture files."""
    for name in os.listdir(fixture_path):
        if name.startswith(prefix) and name.endswith(".json"):
            os.system("%s loaddata %s" % (manage_command, os.path.join(fixture_path, name)))


def syncdb(manage_command):
    """sync db."""
    print "syncing and migrating db..."
    os.system("%s syncdb --noinput --migrate --verbosity 0" % manage_command)
    os.system("%s clear_cache" % manage_command)


def main(argv):
    """main function."""
    instance_type = None
    heroku_app = None
    manage_command = "python manage.py"
    fixture_path = "fixtures"

    try:
        opts, args = getopt.getopt(argv, "t:r:h", ["type=", "heroku=", "help"])
    except getopt.GetoptError:
        exit_with_help()

    if not opts:
        exit_with_help()

    for opt in opts:
        if opt[0] == "-h" or opt[0] == "--help":
            exit_with_help()
        if opt[0] == "-t" or opt[0] == "--type":
            instance_type = opt[1]
        if opt[0] == "-r" or opt[0] == "--heroku":
            heroku_app = opt[1]
            manage_command = "heroku run --app %s python makahiki/manage.py" % heroku_app
            fixture_path = "makahiki/fixtures"

    if not instance_type in ("default", "demo", "test"):
        exit_with_help()

    _ = args

    install_requirements(heroku_app)

    reset_db(heroku_app)

    syncdb(manage_command)

    copy_static_media(manage_command, heroku_app)

    print "loading base data..."
    load_fixtures(manage_command, fixture_path, "base_")

    if instance_type == "demo":
        print "setting up demo data..."
        load_fixtures(manage_command, fixture_path, "demo_")
        # setup 2 user per team, and 1 one-week round
        os.system("%s setup_test_data all 2 1" % manage_command)

    if instance_type == "test":
        print "setting up test data..."
        load_fixtures(manage_command, fixture_path, "test_")
        # setup 2 user per team, and 3 one-week round
        os.system("%s setup_test_data all 2 3" % manage_command)


if __name__ == '__main__':
    main(sys.argv[1:])
