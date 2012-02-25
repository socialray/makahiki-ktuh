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
SITE_NAME = "UHM"
CONTACT_EMAIL = "feedback@kukuicup.org"
ADMINS = (("Makahiki Developers", "makahiki-dev@googlegroups.com"),)
MANAGERS = ADMINS

#####################
# COMPETITION
#####################
# The actual name of the competition.
COMPETITION_NAME = "Kukui Cup"

# Optional setting to specify a special name for the points. Default is "point".
COMPETITION_POINT_LABEL = "point"

# The label of a standard competition team.  Defaults to "Team" if this is not provided.
COMPETITION_TEAM_LABEL = "Lounge"

# This include start and end dates along with round information.
# The start and end date of the competition.
COMPETITION_START = (datetime.date.today() - datetime.timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
COMPETITION_END = (datetime.date.today() + datetime.timedelta(days=6)).strftime("%Y-%m-%d %H:%M:%S")

# The rounds of the competition. Specify dates using "yyyy-mm-dd hh:mm:ss".
# Start means the competition will start at midnight on that date.
# End means the competition will end at midnight of that date.
# This means that a round that ends on "2010-08-02" will end at 11:59pm of August 1st.
COMPETITION_ROUNDS = {
    "Round 1": {
        "start": (datetime.date.today() - datetime.timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S"),
        "end": (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
        },
    }

###################
# Authentication
###################
# Settings for the CAS authentication service.
CAS_SERVER_URL = 'https://login.its.hawaii.edu/cas/'

##################
# DATA Settings
##################
# This is the name of the activity in the setup wizard.
# If the user answers that question correctly, this activity will be marked as completed.
SETUP_WIZARD_ACTIVITY_NAME = "Intro video"

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
LOCALE_SETTING = 'en_US.UTF-8'

###################
# THEME
###################
# The theme to use as default. This corresponds to a folder in media that contains the CSS.
MAKAHIKI_THEME = "default"
