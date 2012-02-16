"""
 game_settings.py
 This file contains organizational-level settings for the game.
 These settings include the name of the game, competition start/end date, authentication,
 and theme settings.
"""

import datetime

#####################
# SITE
#####################
SITE_ID = 1
SITE_NAME = "Kukui Cup"
CONTACT_EMAIL = "feedback@example.com"
ADMINS = (("Makahiki Developers", "makahiki-dev@googlegroups.com"),)
MANAGERS = ADMINS

#####################
# COMPETITION
#####################
# The actual name of the competition.
COMPETITION_NAME = "Kukui Cup"

# Optional setting to specify a special name for the points. Default is "points".
COMPETITION_POINT_NAME = "point"

# The name of a standard competition grouping.  Defaults to "Team" if this is not provided.
COMPETITION_GROUP_NAME = "Lounge"

# This include start and end dates along with round information.
# The start and end date of the competition.
COMPETITION_START = (datetime.date.today() - datetime.timedelta(days=3)).strftime("%Y-%m-%d")
COMPETITION_END = (datetime.date.today() + datetime.timedelta(days=6)).strftime("%Y-%m-%d")

# The rounds of the competition. Specify dates using "yyyy-mm-dd".
# Start means the competition will start at midnight on that date.
# End means the competition will end at midnight of that date.
# This means that a round that ends on "2010-08-02" will end at 11:59pm of August 1st.
COMPETITION_ROUNDS = {
    "Round 1": {
        "start": (datetime.date.today() - datetime.timedelta(days=3)).strftime("%Y-%m-%d"),
        "end": (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
        },
    }

POINTS_PER_TICKET = 20

###################
# Authentication
###################
# Settings for the CAS authentication service.
CAS_SERVER_URL = 'https://login.its.hawaii.edu/cas/'
CAS_REDIRECT_URL = '/home'
CAS_IGNORE_REFERER = True

LOGIN_URL = "/account/cas/login/"
LOGIN_REDIRECT_URLNAME = "home_index"
LOGIN_REDIRECT_URL = "/"
RESTRICTED_URL = '/restricted/'

# When enabled, users who try to access the site before or after the competition ends are blocked.
# Admin users are able to log in at any time.
CAN_ACCESS_OUTSIDE_COMPETITION = False

##################
# DATA Settings
##################
# This is the name of the activity in the setup wizard.
# If the user answers that question correctly, this activity will be marked as completed.
SETUP_WIZARD_ACTIVITY_NAME = "Intro video"

# This is the url to the last 30 days spreadsheet.
ENERGY_THIRTY_DAYS_URL = "https://spreadsheets.google.com/spreadsheet/tq?key=" \
                         "0An9ynmXUoikYdHhxeW1xRURQZUlGd1oxVERnQktsWXc"

# This is the url to th energy goal game spreadsheet.
ENERGY_GOAL_URL = "https://spreadsheets.google.com/spreadsheet/tq?key=" \
                  "0An9ynmXUoikYdEdmU21FaWtlSlNSSnQ3YmNxUFBWaFE"

POWER_GAUGE_URL = "https://spreadsheets.google.com/tq?key=" \
                  "0An9ynmXUoikYdEx3TkRkYjdwdHZkTUo4OGI4NVZ3cmc"

###################
# TIME_ZONE
###################
# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Pacific/Honolulu'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en'

# Locale setting for currency conversion.
LOCALE_SETTING = ''

###################
# THEME
###################

# The theme to use as default. This corresponds to a folder in media that contains the CSS.
MAKAHIKI_THEME = "default"

CSS_THEME = "default"
