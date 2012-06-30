#!/usr/bin/python

"""
Invocation:  scripts/initialize_instance .py -t|--type[=] default|demo|test
                                             -r|--heroku[=] <heroku_app>
                                             -u|--update

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
  * re-create the database and database user
  * Synchronize and migrates the database schemas.
  * Collects and copies the static and media files to the specific location.
  * Loads the default or test configuration of data.

if -u or --update is specified, it will only update the instance, i.e., update the
requirements, synchronize and migrate the database, copy static and media files.

"""

import getopt

import os
import sys


def exit_with_help():
    """Print usage of the command, then exit with error code."""
    print __doc__
    sys.exit(2)


def copy_static_media(heroku_app):
    """copy static media."""
    print "collecting static and media files..."
    os.system("python manage.py collectstatic --noinput --verbosity 0")

    if not heroku_app:
        os.system("cp -r media site_media")
    else:
        # always use S3 in heorku, need to upload the media directory to S3 bucket
        command = "s3put -a %s -s %s -b %s -g public-read -p `pwd` %s" % (
            os.environ['MAKAHIKI_AWS_ACCESS_KEY_ID'],
            os.environ['MAKAHIKI_AWS_SECRET_ACCESS_KEY'],
            heroku_app,
            "media"
            )
        #print command
        os.system(command)
        command = "s3put -a %s -s %s -b %s -g public-read -p `pwd`/site_media %s" % (
            os.environ['MAKAHIKI_AWS_ACCESS_KEY_ID'],
            os.environ['MAKAHIKI_AWS_SECRET_ACCESS_KEY'],
            heroku_app,
            "site_media/static"
            )
        #print command
        os.system(command)


def reset_db(heroku_app):
    """reset db."""
    print "WARNING: This command will reset the database. " \
          "All existing data will be deleted. This process is irreversible.\n"
    value = raw_input("Do you wish to continue (Y/n)? ")
    while value != "Y" and value != "n":
        print "Invalid option %s\n" % value
        value = raw_input("Do you wish to continue (Y/n)? ")
    if value == "n":
        print "Operation cancelled.\n"
        sys.exit(2)

    print "resetting the db..."
    if not heroku_app:
        os.system("python scripts/initialize_postgres.py")
    else:
        os.system("heroku pg:reset SHARED_DATABASE --app %s  --confirm %s" % (
            heroku_app, heroku_app))


def install_requirements():
    """install requirements."""
    print "installing requirements..."
    os.system("pip install -r ../requirements.txt --quiet")


def create_heroku_app(heroku_app):
    """create the heroku application."""
    print "create heroku app..."
    os.system("heroku create %s --stack cedar --remote %s" % (heroku_app, heroku_app))

    os.system("heroku config:add --app $1 MAKAHIKI_ADMIN_INFO=$MAKAHIKI_ADMIN_INFO "\
                "MAKAHIKI_USE_MEMCACHED=$MAKAHIKI_USE_MEMCACHED "\
                "MAKAHIKI_USE_HEROKU=True "\
                "MAKAHIKI_USE_S3=$MAKAHIKI_USE_S3 "\
                "MAKAHIKI_AWS_ACCESS_KEY_ID=$MAKAHIKI_AWS_ACCESS_KEY_ID "\
                "MAKAHIKI_AWS_SECRET_ACCESS_KEY=$MAKAHIKI_AWS_SECRET_ACCESS_KEY "\
                "MAKAHIKI_AWS_STORAGE_BUCKET_NAME=%s "\
                "MAKAHIKI_EMAIL_INFO=$MAKAHIKI_EMAIL_INFO "\
                "MAKAHIKI_USE_FACEBOOK=$MAKAHIKI_USE_FACEBOOK "\
                "MAKAHIKI_FACEBOOK_APP_ID=$MAKAHIKI_FACEBOOK_APP_ID "\
                "MAKAHIKI_FACEBOOK_SECRET_KEY=$MAKAHIKI_FACEBOOK_SECRET_KEY" % heroku_app)

    os.system("heroku addons:add --app %s memcache" % heroku_app)


def push_to_heroku(heroku_app):
    """push to heroku."""
    print "push to heroku..."
    os.system("git push %s master" % heroku_app)


def create_or_update_heroku(heroku_app, is_update_only):
    """create or update heroku."""
    if not is_update_only:
        create_heroku_app(heroku_app)
    else:
        push_to_heroku(heroku_app)


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


def load_data(manage_command, instance_type, fixture_path):
    """load fixture and test data."""

    print "loading base data..."
    load_fixtures(manage_command, fixture_path, "base_")

    if instance_type == "demo":
        print "setting up demo data..."
        load_fixtures(manage_command, fixture_path, "demo_")
        # setup 2 user per team, and 1 one-week round
        os.system("%s setup_test_data all 2 1" % manage_command)
        # change the commitment duration to 1 day
        os.system("%s setup_test_data commitment_durations 1" % manage_command)

    if instance_type == "test":
        print "setting up test data..."
        load_fixtures(manage_command, fixture_path, "test_")
        # setup 2 user per team, and 3 one-week round
        os.system("%s setup_test_data all 2 3" % manage_command)


def main(argv):
    """main function."""
    instance_type = None
    heroku_app = None
    is_update_only = False
    manage_command = "python manage.py"
    fixture_path = "fixtures"

    try:
        opts, args = getopt.getopt(argv, "t:r:hu", ["type=", "heroku=", "help", "update"])
    except getopt.GetoptError:
        exit_with_help()

    if not opts:
        exit_with_help()

    for opt in opts:
        if opt[0] == "-h" or opt[0] == "--help":
            exit_with_help()
        if opt[0] == "-u" or opt[0] == "--update":
            is_update_only = True
        if opt[0] == "-t" or opt[0] == "--type":
            instance_type = opt[1]
        if opt[0] == "-r" or opt[0] == "--heroku":
            heroku_app = opt[1]
            manage_command = "heroku run --app %s python makahiki/manage.py" % heroku_app
            fixture_path = "makahiki/fixtures"

    if not instance_type in ("default", "demo", "test") and not is_update_only:
        exit_with_help()

    _ = args

    if not heroku_app:
        install_requirements()
    else:
        create_or_update_heroku(heroku_app, is_update_only)

    if not is_update_only:
        reset_db(heroku_app)

    syncdb(manage_command)

    copy_static_media(heroku_app)

    if not is_update_only:
        load_data(manage_command, instance_type, fixture_path)


if __name__ == '__main__':
    main(sys.argv[1:])
