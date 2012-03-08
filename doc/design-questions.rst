Design Questions
================

Click on section title to go to corresponding documentation.

:mod:`apps.managers.cache_mgr`
------------------------------

  * Does this provide facilities for memcached management?

:mod:`apps.managers.auth_mgr`
-----------------------------

  * For Makahiki2, we need a more flexible mechanism for authentication, including CAS, OpenDirectory, and "manual".  Should the authentication manager implement support for multiple authentication schemes?   How will this interact with the user interface for authentication?

:mod:`apps.managers.log_mgr`
----------------------------

  * Should we have a set of prepackaged log file analyses?  If so, where do they go?  scripts/?  admin interface? management command? (More generally, when should something be a script vs. a management commmand vs. an admin form?)

:mod:`apps.managers.player_mgr`
-------------------------------

  * Model fields should be documented.
  * Model hardwires the point systems in use. 
  * Management commands to load and reset users need unit tests.
  * Score data (referral bonus, points) directly in model.

:mod:`apps.managers.score_mgr`
------------------------------

  * Does not appear to support definition of new scoring systems (such as 'gallons' for water).
  * Should the score manager have an internal data structure containing the current state of all scores for all users and teams that is queried by modules?  Or should each player have an instance of a scoring system that provides their own personal data?

:mod:`apps.managers.settings_mgr`
---------------------------------

  * Where should one specify the organizational logo that goes in the header bar?
  * Should competition_point_label be provided by scoring_mgr? 
  * Should competition_team_label be provided by team_mgr?
  * Should cas_server_url be provided by auth_mgr?
  * Lots of settings defined in init.py.  Is this appropriate?
  * The tests.py file does not appear to be invoked during testing.  Is the
    indentation wrong?

:mod:`apps.managers.team_mgr`
-----------------------------

  * Do we want to hardwire methods to get a particular scoring system (points)?  In the case of EWC, the "team" will also have a score related to gallons and kWh.

:mod:`apps.widgets.badges`
--------------------------

  * Currently we only have three possible badges.  That seems lame; can we think of more?

 















