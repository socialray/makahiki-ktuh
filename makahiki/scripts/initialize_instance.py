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
    os.system("rm -rf site_media/media; mkdir site_media/media; "
              "mv site_media/static/media site_media/media")


if __name__ == '__main__':
    main()
