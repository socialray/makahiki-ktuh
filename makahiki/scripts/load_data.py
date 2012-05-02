#!/usr/bin/python

"""load initial data into makahiki system.

When the system is stable, could run python manage.py loaddata fixturs/* to load everything
there.
"""

import os


def main():
    """main function."""
    fixture_path = "fixtures"

    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "base_teams.json"))
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "base_activities.json"))
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "base_quests.json"))
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "base_help.json"))
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "base_pages.json"))
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "base_settings.json"))
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "base_resource.json"))
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "test_users.json"))
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "test_energy_goals.json"))
    os.system("python manage.py loaddata %s" % os.path.join(fixture_path, "test_prizes.json"))


if __name__ == '__main__':
    main()
