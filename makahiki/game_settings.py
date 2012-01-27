# makahiki_settings.py
# This file contains organizational-level settings for the competition.
# These settings include the name of the competition and theme settings.

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
# Overrides time zone specified in settings.py
TIME_ZONE = 'Pacific/Honolulu'

# Settings for the CAS authentication service.
CAS_SERVER_URL = 'https://login.its.hawaii.edu/cas/'
CAS_REDIRECT_URL = '/home'
CAS_IGNORE_REFERER = True

# The actual name of the competition.
COMPETITION_NAME = "Kukui Cup"

# Optional setting to specify a special name for the points. Default is "points".
COMPETITION_POINT_NAME = "point"

# The name of a standard competition grouping.  Defaults to "Floor" if this is not provided.
COMPETITION_GROUP_NAME = "Lounge"

# Enable the CSS theme selector at the top of the page.
ENABLE_CSS_SELECTOR = False

# The theme to use as default. This corresponds to a folder in media that contains the CSS.
MAKAHIKI_THEME = "default"

CSS_THEME = "default"

# Kukui Cup Template theme setting.
MAKAHIKI_TEMPLATE_THEME = 'default'

# Theme settings for Makahiki.  Used to aid in styling the Javascript widgets.
# The system will insert the colors based on the selected theme.  If an entry
# for a theme does not exist, default will be used.
MAKAHIKI_THEME_SETTINGS = {
    "default" : {
        "widgetBackgroundColor" : 'F5F3E5',
        "widgetHeaderColor" : '459E00',
        "widgetHeaderTextColor" : 'white',
        "widgetTextColor" : '312E25',
        "widgetTextFont" : 'Ariel, sans serif',
        "windowNavBarColor" : '2F6B00',
        },
    "cupertino" : {
        "widgetBackgroundColor" : 'F2F5F7',
        "widgetHeaderColor" : '459E00',
        "widgetHeaderTextColor" : 'white',
        "widgetTextColor" : '312E25',
        "widgetTextFont" : 'Ariel, sans serif',
        "windowNavBarColor" : '2F6B00',
        },
    "start" : {
        "widgetBackgroundColor" : 'fff',
        "widgetHeaderColor" : '459E00',
        "widgetHeaderTextColor" : 'white',
        "widgetTextColor" : '312E25',
        "widgetTextFont" : 'Ariel, sans serif',
        "windowNavBarColor" : '2F6B00',
        },
    }

# This is the name of the activity in the setup wizard.
# If the user answers that question correctly, this activity will be marked as completed.
SETUP_WIZARD_ACTIVITY_NAME = "Intro video"

# This is the url to the last 30 days spreadsheet.
ENERGY_THIRTY_DAYS_URL = "https://spreadsheets.google.com/spreadsheet/tq?key=0An9ynmXUoikYdHhxeW1xRURQZUlGd1oxVERnQktsWXc"

# This is the url to th energy goal game spreadsheet.
ENERGY_GOAL_URL = "https://spreadsheets.google.com/spreadsheet/tq?key=0An9ynmXUoikYdEdmU21FaWtlSlNSSnQ3YmNxUFBWaFE"

POWER_GAUGE_URL = "https://spreadsheets.google.com/tq?key=0An9ynmXUoikYdEx3TkRkYjdwdHZkTUo4OGI4NVZ3cmc"

# competition_settings.py
# This file contains settings for the current competition.
# This include start and end dates along with round information.
import datetime # Only used to dynamically set the round dates.

# The start and end date of the competition.
COMPETITION_START = (datetime.date.today() - datetime.timedelta(days=3)).strftime("%Y-%m-%d")
COMPETITION_END = (datetime.date.today() + datetime.timedelta(days=6)).strftime("%Y-%m-%d")

# The rounds of the competition. Specify dates using "yyyy-mm-dd".
# Start means the competition will start at midnight on that date.
# End means the competition will end at midnight of that date.
# This means that a round that ends on "2010-08-02" will end at 11:59pm of August 1st.
COMPETITION_ROUNDS = {
    "Round 1" : {
        "start": (datetime.date.today() - datetime.timedelta(days=3)).strftime("%Y-%m-%d"),
        "end": (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
        },
    }

# When enabled, users who try to access the site before or after the competition ends are blocked.
# Admin users are able to log in at any time.
CAN_ACCESS_OUTSIDE_COMPETITION = False

###############################################
# PAGE LAYOUT SETTINGS
###############################################
WIDTHS = {
    "default"          : 1024,
    "large"            : 2048,
    "tablet_portrait"  : 500,
    "tablet_landscape" : 768,
    "phone_portrait"   : 240,
    "phone_landscape"  : 320,
}
