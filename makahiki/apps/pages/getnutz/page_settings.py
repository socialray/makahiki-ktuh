PAGE_TITLE = "Get Nutz"
BASE_TEMPLATE = "logged_in_base.html"
CSS = "getnutz"

# LAYOUTS FORMAT:
# 'SCREEN_WIDTH' : ( ("gamelets", 0.3)
LAYOUTS = {
    'DEFAULT' : ( ("home", 1),
                  (("upcoming_events", 0.3), ("smartgrid_game", 0.7)),
                ),
    }
