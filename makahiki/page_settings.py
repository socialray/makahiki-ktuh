PAGE_SETTINGS = {
    "actions" : { "PAGE_TITLE" : "Actions",
                  "BASE_TEMPLATE" : "logged_in_base.html",
                  "LAYOUTS" : {
                                'DEFAULT' : ( ("scoreboard", "100%"),
                                              (("upcoming_events", "40%"),  ("smartgrid", "60%"),),
                                            ),
                                'PHONE_PORTRAIT' : ( ("upcoming_events", "100%"),
                                                     ("smartgrid", "100%"),
                                                     ("scoreboard", "100%"),
                                                   ),
                              },
                },
}
