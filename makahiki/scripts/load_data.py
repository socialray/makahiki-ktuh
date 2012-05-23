#!/usr/bin/python

"""Invocation:  scripts/load_data

Loads the default configuration of data into makahiki.

Note: when the system is stable, could simply run python manage.py loaddata fixtures/* 
"""

import os


def main():
    """main function."""
    fixture_path = "fixtures"

    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "base_help.json"))
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "base_pages.json"))
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "base_quests.json"))
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "base_resource.json"))
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "base_settings.json"))
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "base_smartgrid.json"))
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "test_teams.json"))
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "test_prizes.json"))
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "test_users.json"))

if __name__ == '__main__':
    main()
