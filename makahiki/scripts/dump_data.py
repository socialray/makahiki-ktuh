#!/usr/bin/python

"""load initial data into makahiki system.

When the system is stable, could run python manage.py loaddata fixturs/* to load everything
there.
"""

import os

def main():
    fixture_path = "fixtures"

    os.system("python manage.py dumpdata --indent=4 team_mgr.group team_mgr.team " \
              "> %s" % os.path.join(fixture_path, "base_teams.json"))
    os.system("python manage.py dumpdata --indent=4 smartgrid.category smartgrid.activity " \
              "smartgrid.commitment smartgrid.activitybase smartgrid.questionchoice " \
              "smartgrid.textpromptquestion " \
              "> %s" % os.path.join(fixture_path, "base_activities.json"))
    os.system("python manage.py dumpdata --indent=4 quests " \
              "> %s" % os.path.join(fixture_path, "base_quests.json"))
    os.system("python manage.py dumpdata --indent=4 help_mgr " \
              "> %s" % os.path.join(fixture_path, "base_help.json"))
    os.system("python manage.py dumpdata --indent=4 auth.user player_mgr " \
              "> %s" % os.path.join(fixture_path, "test_users.json"))
    os.system("python manage.py dumpdata --indent=4 energy_goal " \
              "> %s" % os.path.join(fixture_path, "test_energy_goals.json"))
    os.system("python manage.py dumpdata --indent=4 energy_power_meter " \
              "> %s" % os.path.join(fixture_path, "test_energy_power_meter.json"))
    os.system("python manage.py dumpdata --indent=4 energy_scoreboard " \
              "> %s" % os.path.join(fixture_path, "test_energy_data.json"))
    os.system("python manage.py dumpdata --indent=4 prizes raffle " \
              "> %s" % os.path.join(fixture_path, "test_prizes.json"))
    os.system("python manage.py dumpdata --indent=4 settings_mgr.challengesettings settings_mgr.pagesettings " \
              "> %s" % os.path.join(fixture_path, "base_settings.json"))


if __name__ == '__main__':
    main()


