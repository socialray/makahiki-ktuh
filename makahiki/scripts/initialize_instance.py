#!/usr/bin/python

"""Invocation:  scripts/initialize_instance .py [--type=[default|demo|test]]
Use this script to create an instance with different types of configuration:
[default]: includes all the basic configuration. User will need to create the round info,
           resource settings, resource goal settings, team, etc.
[demo]:  includes all the "default" configuration, with the additions of demo information, such
         as rounds, resource and goal settings, demo team, demo users, and use internal
         authentication.
[test]:  similar to "demo" configuration, with the additions of more test users and use
         CAS authentication instead of internal authentication.

Defaults to creating an instance with the default configuration.

Performs the following:
  * Updates and/or installation of any modules in requirements.txt
  * Syncs the database and migrates the database schemas.
  * Collects and copies the static and media files to the desired location.
  * Creates the specified challenge.
  * Loads the default or test configuration of data.
  """
import getopt

import os
import sys


def main(argv):
    """main function."""
    instance_type = "default"

    try:
        opts, args = getopt.getopt(argv, "t:", ["type="])
    except getopt.GetoptError:
        print "Usage: initialize_instance.py [-t|--type=[default|demo|test]]"
        sys.exit(2)

    for opt in opts:
        if opt[0] == "-t" or opt[0] == "--type":
            instance_type = opt[1]

    _ = args

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

    print "loading base data..."
    fixture_path = "fixtures"
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "base_*.json"))

    if instance_type == "demo" or instance_type == "test":
        print "setting up demo data..."
        os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "demo_*.json"))
        os.system("python manage.py setup_test_data all")

    if instance_type == "test":
        print "setting up test data..."
        os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "test_*.json"))


if __name__ == '__main__':
    main(sys.argv[1:])
