#!/usr/bin/python

"""Invocation:  scripts/initialize_instance
Useful for initial configuration of a makahiki instance, and for re-configuration after
pulling changes from the repository.

Performs the following:
  * Updates and/or installation of any modules in requirements.txt
  * Syncs the database.
  * Migrates the database schemas.
  * Loads the default configuration of data (via scripts/load_data)
  * Reinitializes the test users and sets up test data.
  * Deals with static media locations.
  """
import getopt

import os
import sys


def main(argv):
    """main function."""
    type = "default"

    try:
        opts, args = getopt.getopt(argv, "t:", ["type="])
    except getopt.GetoptError:
        print "Usage: initialize_instance.py [-t|--type=[default|test]] <site_name>"
        sys.exit(2)

    for opt in opts:
        if opt[0] == "-t" or opt[0] == "--type":
            type = opt[1]

    if len(args) == 0:
        print "Please specify a site_name for the instance."
        sys.exit(2)

    site_name = args[0]

    print "installing requirements..."
    os.system("pip install -r ../requirements.txt --quiet")

    print "syncing and migrating db..."
    os.system("python manage.py syncdb --noinput --migrate --verbosity 0")

    print "collecting static and media files..."
    os.system("python manage.py collectstatic --noinput --verbosity 0")
    os.system("cp -r media site_media")

    if 'MAKAHIKI_USE_S3' in os.environ and \
        os.environ['MAKAHIKI_USE_S3'].lower() == 'true':
        # if use S3, need to upload the media directory to S3 bucket
        command = "s3put -a %s -s %s -b %s -p `pwd` %s" % (
            os.environ['MAKAHIKI_AWS_ACCESS_KEY_ID'],
            os.environ['MAKAHIKI_AWS_SECRET_ACCESS_KEY'],
            os.environ['MAKAHIKI_AWS_STORAGE_BUCKET_NAME'],
            "media"
        )
        print command
        os.system(command)

    print "creating the challenge..."
    os.system("python manage.py create_challenge %s" % site_name)

    print "loading base data..."
    fixture_path = "fixtures"
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "base_help.json"))
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "base_pages.json"))
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "base_quests.json"))
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "base_settings.json"))
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "base_smartgrid.json"))

    if type == "test":
        print "setting up test data..."
        os.system("python manage.py loaddata %s" % os.path.join(fixture_path,
                                                                "test_challenge.json"))
        os.system("python manage.py loaddata %s" % os.path.join(fixture_path,
                                                                "test_prizes.json"))
        os.system("python manage.py loaddata %s" % os.path.join(fixture_path,
                                                                "test_smartgrid_events.json"))
        os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "test_teams.json"))
        os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "test_users.json"))

        os.system("python manage.py setup_test_data all")

    # set the site_name


if __name__ == '__main__':
    main(sys.argv[1:])
