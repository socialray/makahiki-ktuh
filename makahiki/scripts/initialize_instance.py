#!/usr/bin/python

"""initialize the makahiki instance."""

import os


def main():
    """main function."""

    os.system("pip install -r ../requirements.txt")
    os.system("python manage.py syncdb --noinput")
    os.system("python manage.py migrate")
    os.system("python scripts/load_data.py")
    os.system("python manage.py collectstatic --noinput")
    os.system("cp -r media site_media")
    # if use S3, need to upload the media directory to S3 bucket

if __name__ == '__main__':
    main()
