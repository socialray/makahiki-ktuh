#!/usr/bin/python

"""Invocation:  scripts/load_data

Loads the default configuration of data into makahiki.

Note: when the system is stable, could simply run python manage.py loaddata fixtures/*
"""

import os


def main():
    """main function."""
    fixture_path = "fixtures"

    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "base_*.json"))
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "demo_*.json"))
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "test_*.json"))


if __name__ == '__main__':
    main()
