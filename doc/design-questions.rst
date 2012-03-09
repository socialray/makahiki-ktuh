Design Questions
================

Click on section title to go to corresponding documentation.

:mod:`apps.managers.cache_mgr`
------------------------------

  1. Does this provide facilities for memcached management?

:mod:`apps.managers.auth_mgr`
-----------------------------

  1. For Makahiki2, we need a more flexible mechanism for authentication, including CAS, OpenDirectory, and "manual".  Should the authentication manager implement support for multiple authentication schemes?   How will this interact with the user interface for authentication?

:mod:`apps.managers.log_mgr`
----------------------------

  1. Should we have a set of prepackaged log file analyses?  If so, where do they go?  scripts/?  admin interface? management command? (More generally, when should something be a script vs. a management commmand vs. an admin form?)

:mod:`apps.managers.player_mgr`
-------------------------------

  1. Model fields should be documented.
  2. Model hardwires the point systems in use. 
  3. Management commands to load and reset users need unit tests.
  4. Score data (referral bonus, points) directly in model.

:mod:`apps.managers.score_mgr`
------------------------------

  1. Does not appear to support definition of new scoring systems (such as 'gallons' for water).
  2. Should the score manager have an internal data structure containing the current state of all scores for all users and teams that is queried by modules?  Or should each player have an instance of a scoring system that provides their own personal data?

:mod:`apps.managers.settings_mgr`
---------------------------------

  1. Where should one specify the organizational logo that goes in the header bar?
  2. Should competition_point_label be provided by scoring_mgr? 
  3. Should competition_team_label be provided by team_mgr?
  4. Should cas_server_url be provided by auth_mgr?
  5. Lots of settings defined in init.py.  Is this appropriate?
  6. The tests.py file does not appear to be invoked during testing.  Is  the indentation wrong?

:mod:`apps.managers.team_mgr`
-----------------------------

  1. Do we want to hardwire methods to get a particular scoring system (points)?  In the case of EWC, the "team" will also have a score related to gallons and kWh.


:mod:`apps.widgets.ask_admin`
-----------------------------

  1. The views module hardwires the address for admins. 

:mod:`apps.widgets.badges`
--------------------------

  1. Currently we only have three possible badges.  That seems lame; can we think of more?

:mod:`apps.widgets.energy_goal`
-------------------------------

  1. Should the "manual" energy goal widget be a variant of this module, or
     a separate widget (apps.widgets.manual_energy_goal).   Perhaps even
     more interestingly, since EWC will have a water challenge, maybe the manual
     widget should be able to be instantiated for either water or energy?
  2. It's not really clear how/when energy goal points get awarded.  Is there a
     periodic script that gets run each night?  Where is that code? Can we
     put it in this module?

:mod:`apps.widgets.energy_power_meter`
--------------------------------------

  1. This widget appears to save energy data locally (as part of the
     model).  Is this a change from Makahiki 1? Do we need to be persisting this data, or can we just keep it in-memory?

:mod:`apps.widgets.energy_scoreboard`
-------------------------------------

  1. What does the admin interface to this actually accomplish? (Similar question for other energy widgets?)







