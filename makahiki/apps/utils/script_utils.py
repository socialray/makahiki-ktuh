"""utility methods for makahiki scripts."""

import os
import sys


def exit_with_help(msg):
    """Print usage of the command, then exit with error code."""
    print msg
    sys.exit(2)


def copy_static_media(heroku_app):
    """copy static media."""
    print "collecting static and media files..."
    os.system("rm -rf site_media/static")

    os.system("python manage.py collectstatic --noinput --verbosity 0")

    if not heroku_app:
        os.system("cp -r media site_media")
    else:
        # always use S3 in heorku, need to upload the media directory to S3 bucket
        if 'MAKAHIKI_AWS_ACCESS_KEY_ID' in os.environ and\
           'MAKAHIKI_AWS_SECRET_ACCESS_KEY' in os.environ:
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
        else:
            print "Environment variable MAKAHIKI_AWS_ACCESS_KEY_ID and/or " \
                  "MAKAHIKI_AWS_SECRET_ACCESS_KEY not defined. Exiting."
            sys.exit(1)


def install_requirements():
    """install requirements."""
    print "installing requirements..."
    os.system("pip install -r ../requirements.txt --quiet")


def push_to_heroku(heroku_app):
    """push to heroku."""
    print "push to heroku..."
    os.system("git push %s master" % heroku_app)


def syncdb(manage_command):
    """sync db."""
    print "syncing and migrating db..."
    os.system("%s syncdb --noinput --migrate --verbosity 0" % manage_command)
    os.system("%s clear_cache" % manage_command)


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
        os.system("heroku pg:reset HEROKU_POSTGRESQL_AQUA --app %s  --confirm %s" % (
            heroku_app, heroku_app))


def create_heroku_app(heroku_app):
    """create the heroku application."""
    print "create heroku app..."
    os.system("heroku labs:enable default-heroku-postgresql-dev")
    os.system("heroku create %s --stack cedar --remote %s" % (heroku_app, heroku_app))
    os.system("git remote add %s git@heroku.com:%s.git" % (heroku_app, heroku_app))

    os.system("heroku config:add --app %s MAKAHIKI_ADMIN_INFO=$MAKAHIKI_ADMIN_INFO "\
                "MAKAHIKI_USE_MEMCACHED=$MAKAHIKI_USE_MEMCACHED "\
                "MAKAHIKI_USE_HEROKU=True "\
                "MAKAHIKI_USE_S3=$MAKAHIKI_USE_S3 "\
                "MAKAHIKI_AWS_ACCESS_KEY_ID=$MAKAHIKI_AWS_ACCESS_KEY_ID "\
                "MAKAHIKI_AWS_SECRET_ACCESS_KEY=$MAKAHIKI_AWS_SECRET_ACCESS_KEY "\
                "MAKAHIKI_AWS_STORAGE_BUCKET_NAME=%s "\
                "MAKAHIKI_EMAIL_INFO=$MAKAHIKI_EMAIL_INFO "\
                "MAKAHIKI_USE_FACEBOOK=$MAKAHIKI_USE_FACEBOOK "\
                "MAKAHIKI_FACEBOOK_APP_ID=$MAKAHIKI_FACEBOOK_APP_ID "\
                "MAKAHIKI_FACEBOOK_SECRET_KEY=$MAKAHIKI_FACEBOOK_SECRET_KEY" % (heroku_app,
                                                                                heroku_app))

    os.system("heroku addons:add --app %s memcache" % heroku_app)


def load_fixtures(manage_command, fixture_path, prefix):
    """load fixture files."""
    for name in os.listdir(fixture_path):
        if name.startswith(prefix) and name.endswith(".json"):
            fixture = os.path.join(fixture_path, name)
            if manage_command.startswith("heroku"):
                fixture = os.path.join("makahiki", fixture)
            print "loading fixture %s..." % name
            os.system("%s loaddata -v 0 %s" % (manage_command, fixture))


def load_data(manage_command, instance_type, fixture_path):
    """load fixture and test data."""

    print "loading base data..."
    load_fixtures(manage_command, fixture_path, "base_")

    if instance_type == "default":
        print "setting up default data..."
        os.system("%s setup_test_data rounds 1" % manage_command)
        load_fixtures(manage_command, fixture_path, "default_")
    elif instance_type == "demo":
        print "setting up demo data..."
        os.system("%s setup_test_data rounds 1" % manage_command)
        load_fixtures(manage_command, fixture_path, "demo_")
        # setup 2 user per team
        os.system("%s setup_test_data all 2" % manage_command)
        # change the commitment duration to 1 day
        os.system("%s setup_test_data commitment_durations 1" % manage_command)
    elif instance_type == "test":
        print "setting up test data..."
        os.system("%s setup_test_data rounds 3" % manage_command)
        load_fixtures(manage_command, fixture_path, "test_")
        # setup 2 user per team
        os.system("%s setup_test_data all 2" % manage_command)
    elif instance_type == "uh12":
        print "setting up uh12 data..."
        os.system("%s setup_test_data rounds 4" % manage_command)
        load_fixtures(manage_command, fixture_path, "uh12_")
        # setup 2 user per team
        os.system("%s setup_test_data all 2" % manage_command)
