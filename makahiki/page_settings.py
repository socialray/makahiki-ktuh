"""
page_settings.py
This file contains settings for the page layouts.
"""

###############################################
# PAGE LAYOUT GLOBALs
###############################################
WIDTHS = {
    "DEFAULT": 1024,
    "LARGE": 2048,
    "TABLET_PORTRAIT": 500,
    "TABLET_LANDSCAPE": 768,
    "PHONE_PORTRAIT": 240,
    "PHONE_LANDSCAPE": 320,
    }

###############################################
# PAGE LAYOUT SETTINGS
###############################################
# each page's layout is defined in a dictionary with the page name as the
# key, and another dictionary as the layout settings for the page. The
# settings dictionary includes keys such as "PAGE_TITLE", "BASE_TEMPLATE",
# and "LAYOUTS". LAYOUTS is another dictionary to include layouts for
# different device widths defined above.
# An LAYOUTS example is:
#    { "<WIDTHS>" : ( (("row1_widget1", "40%"), ("row1_widget2", "60%")),
#                     ("row2_widget", "100%") ) }
PAGE_SETTINGS = {
    # home page
    "home":
            {"PAGE_TITLE": "Home",
             "BASE_TEMPLATE": "logged_in_base.html",
             "LAYOUTS":
                     {"DEFAULT":
                          (
                              ("home", "100%"),
                              ),
                      "PHONE_PORTRAIT":
                          (
                              ("home", "100%"),
                              ),
                      },
             },

    # help page
    "help":
            {"PAGE_TITLE": "Help",
             "BASE_TEMPLATE": "logged_in_base.html",
             "LAYOUTS":
                     {"DEFAULT":
                          (
                              (("help_intro", "50%"), ("help_rule", "50%"), ),
                              (("help_faq", "50%"), ("ask_admin", "50%"),),

                              ),
                      "PHONE_PORTRAIT":
                          (
                              ("help_intro", "100%"),
                              ("help_faq", "100%"),
                              ("help_rule", "100%"),
                              ("ask_admin", "100%"),
                              ),
                      },
             },

    }
