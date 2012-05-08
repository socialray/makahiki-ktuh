#!/usr/bin/python

"""initialize the makahiki instance."""

import os


def main():
    """main function."""

    os.system("python manage.py syncdb --noinput")
    os.system("python manage.py migrate")
    os.system("python scripts/load_data.py")

if __name__ == '__main__':
    main()
