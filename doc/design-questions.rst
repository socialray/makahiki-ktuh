Design Questions
================

Click on section title to go to corresponding documentation.

:mod:`apps.managers.cache_mgr`
------------------------------

  1. Does this provide facilities for memcached management?

:mod:`apps.managers.auth_mgr`
-----------------------------

  2. For Makahiki2, we need a more flexible mechanism for authentication, including CAS, OpenDirectory, and "manual".  Should the authentication manager implement support for multiple authentication schemes?   How will this interact with the user interface for authentication?

:mod:`apps.managers.log_mgr`
----------------------------

  3. Should we have a set of prepackaged log file analyses?  If so, where do they go?  scripts/?  admin interface? management command? (More generally, when should something be a script vs. a management commmand vs. an admin form?)

:mod:`apps.managers.player_mgr`
-------------------------------

  4. Model fields should be documented.
  5. Model hardwires the point systems in use. 
  6. Management commands to load and reset users need unit tests.
  7. Score data (referral bonus, points) directly in model.

:mod:`apps.managers.score_mgr`
------------------------------

  8. Does not appear to support definition of new scoring systems (such as 'gallons' for water).
  9. Should the score manager have an internal data structure containing the current state of all scores for all users and teams that is queried by modules?  Or should each player have an instance of a scoring system that provides their own personal data?

:mod:`apps.managers.settings_mgr`
---------------------------------

  10. Where should one specify the organizational logo that goes in the header bar?
  11. Should competition_point_label be provided by scoring_mgr? 
  12. Should competition_team_label be provided by team_mgr?
  13. Should cas_server_url be provided by auth_mgr?
  14. Lots of settings defined in init.py.  Is this appropriate?
  15. The tests.py file does not appear to be invoked during testing.  Is  the indentation wrong?

:mod:`apps.managers.team_mgr`
-----------------------------

  16. Do we want to hardwire methods to get a particular scoring system (points)?  In the case of EWC, the "team" will also have a score related to gallons and kWh.


:mod:`apps.widgets.ask_admin`
-----------------------------

  17. The views module hardwires the address for admins. 

:mod:`apps.widgets.badges`
--------------------------

  18. Currently we only have three possible badges.  That seems lame; can we think of more?

:mod:`apps.widgets.energy_goal`
-------------------------------

  19. Should the "manual" energy goal widget be a variant of this module, or
      a separate widget (apps.widgets.manual_energy_goal).   Perhaps even
      more interestingly, since EWC will have a water challenge, maybe the manual
      widget should be able to be instantiated for either water or energy?
  20. It's not really clear how/when energy goal points get awarded.  Is there a
      periodic script that gets run each night?  Where is that code? Can we
      put it in this module?

:mod:`apps.widgets.energy_power_meter`
--------------------------------------

  21. This widget appears to save energy data locally (as part of the
      model).  Is this a change from Makahiki 1? Do we need to be persisting this data, or can we just keep it in-memory?

:mod:`apps.widgets.energy_scoreboard`
-------------------------------------

  22. What does the admin interface to this actually accomplish? (Similar question for other energy widgets?)

:mod:`apps.widgets.notifications`
---------------------------------

  23. Three functions in init.py.  Can these be moved elsewhere?

:mod:`apps.widgets.popular_tasks`
---------------------------------

  24. For consistency with new SGG terminology, should this be "popular_actions"?

:mod:`apps.widgets.prizes`
--------------------------

  25. Should the management command for raffle picking and form printing
      move to the raffle widget?

:mod:`apps.widgets.quests`
--------------------------

  26. Should the "utility" functions be in init.py?  More generally, should
      this module be more object-oriented?

:mod:`apps.widgets.scoreboard`
------------------------------

  27. Shouldn't the scoreboard widget refer to the score manager for data?

:mod:`apps.widgets.smartgrid`
------------------------------

  28. Can this code can be restructured and simplified?  Lots going on in init.py.

:mod:`apps.widgets.team_members`
---------------------------------

  29. The team_members widget imports player_mgr but nothing from
      team_mgr.  This seems confusing. Is it correct?
      



High-level issues for discussion
--------------------------------

  A. What is the appropriate level of object orientation?  Should every
     module be implemented via classes? If not, how do we decide when to
     use object orientation and when to not use it?

  B. Unit tests need to be reviewed. It appears that some test classes are
     not even invoked. 
     
  C. When is it appropriate to include methods in init.py?  

  D. When is it appropriate to included methods in urls.py?

  E. When should a feature be part of management.commands, and when should
     it be an external, stand-alone script?








