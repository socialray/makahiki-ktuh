PAGE_NAME = "getnutz"
PAGE_TITLE = "Get Nutz"
BASE_TEMPLATE = "logged_in_base.html"

LAYOUTS = {
    'DEFAULT' : (  ("scoreboard", "100%"),
                  (("upcoming_events", "40%"),  ("smartgrid_game", "60%"),),
                ),
    'PHONE_PORTRAIT' : ( ("upcoming_events", "100%"),
                         ("smartgrid_game", "100%"),
                         ("scoreboard", "100%"),
                       ),
    }
