Design Questions
================

High-level issues for discussion
********************************

  A. What is the appropriate level of object orientation?  Should every
     module be implemented via classes? If not, how do we decide when to
     use object orientation and when to not use it?

  B. Unit tests need to be reviewed. It appears that some test classes are
     not even invoked. 
     
  C. When is it appropriate to include methods in init.py?  

  D. When is it appropriate to included methods in urls.py?

  E. When should a feature be part of management.commands, and when should
     it be an external, stand-alone script?

Is this a framework (yet)?
**************************

After completing this review of the Makahiki 2 codebase, I am struck by the
realization that it does not yet feel like a "framework" or "game engine"
to me.

For me, the defining feature of a domain-specific framework is that domain entities
have a "first class" status within the framework.  In our case, I view at
least the following domain entities as requiring "first class" status for
us to have a framework:

  * Authentication methods
  * Players
  * Teams
  * Scoring systems
  * Widgets

Currently, I do not view any of these entities as having first class status.
For that to be the case, we must have an easy way to perform the following:

  * Create an instance of the entity.
  * Ensure that all instances of the entity have an appropriate, common structure.
  * Be able to determine how many instances of the entity exist.
  * Be able to enable or disable an instance of the entity.
  * Be able to easily extend the system to support new instances of the entity.

Typically, a framework supports the first class status of domain-specific
entities through an object orientation with classes that define
the common structural features and the internal state, and instances
reflecting all the definitions of the entities.   Some first class
entities require persistent state (players, teams), others might not
(authentication systems). 

What I am instead seeing in Makahiki at present is a basically a design in
which a set of methods are triggered by http requests, make calls to an
underlying database, and then return dictionaries of property-value pairs
to pages for display.  (See all of the views.py files for examples.)  This
is simple, but not abstract.  It's very "flat" as an architecture.   For
Makahiki to become a framework, I think we must create and manipulate
domain-specific entities. 

Module specific questions
*************************

Click on the section title to go to corresponding documentation.

:mod:`apps.managers.cache_mgr`
------------------------------

**1. Does this provide facilities for memcached management?**

(Yongwen) No. currently it only provide utilities to invalidate the specific
cache. here are some ideas for improvement:

  - Use first level class CacheMgr instead, extended from Manager base class
  - Public methods:

    - items() - list all cache items
    - get() - get or set cache item
    - invalidate() - invalidate the item
    - invalidate_all()
    - ? restart() - restart cache after the configure
    - ? configure(conf) - programmatically config the cache
    - extend from base class: info() - display cache info and config

(Discussion results)  Can remain as a module (since no state, no instances).  Module will provide an
abstraction layer over underlying cache management system. All calls go through this module.  It can
provide additional helpful utility methods to support common operations.


:mod:`apps.managers.auth_mgr`
-----------------------------

**2. For Makahiki2, we need a more flexible mechanism for authentication, including CAS,
OpenDirectory, and "manual".  Should the authentication manager implement support for
multiple authentication schemes?   How will this interact with the user interface for
authentication?**

(Yongwen) Yes, currently provides CASBackend model and login UI for Django
managed authentication. More backend model could be provided to
support AD, or others.

Create a first level class AuthMgr, with the following methods (examples):
    * backends() - list all configured Backend
    * user_role() - display user's role as admin, staff, etc
    * login_as() - user surrogation (moved from views.py so that view is a pure controller)
    * ? configure(conf) - configure a new backend and add to settings
    * extend from base class: info() - display auth info and config

See authentication sequence email thread for UI related to multiple auth scheme.

(George) It seems to me that "manual" is always present, but we have plugins that take over this functionality. I found a LDAP plugin that should handle open directory at http://code.google.com/p/django-ldap-groups/. Django also supports pluggable authentication backends.

(Discussion)  Not sure if a class is needed ("natural" implementation may not require state or
multiple instances).  Could be implemented as a module and hardwire all supported authentication
schemes. (i.e. authentication might turn out to not be "pluggable" due to complexity of
implementation. Instead, we just document what is needed to do in the code to add support for a new
authentication scheme.).


:mod:`apps.managers.log_mgr`
----------------------------

**3. Should we have a set of prepackaged log file analyses?  If so, where do they go?
scripts/?  admin interface? management command? (More generally, when should something
be a script vs. a management commmand vs. an admin form?)**

(Yongwen) Heroku will have difficulty to write to local filesystem. so, log will
need to be stored in DB. It will serve as the data source for
analytics widget. There might not need any prepackaged log file
analyses.

(George) I think it could be packaged in with mission control, since analyses could be displayed there. Mission control could have an export interface (dump to CSV?) and possibly a management command to do it on the command line.

(Discussion) Some combination of mission control and management command is good. Mission control is
best, since doesn't require command line access.

:mod:`apps.managers.player_mgr`
-------------------------------

**4. Model fields should be documented.**

(Yongwen) Yes.

**5. Model hardwires the point systems in use.**

(Yongwen) The point handling could be encapsulated in score_mgr. Idea:
    * remove points from Profile model
    * all point queries should be from score_mgr
    * add/remove points could be moved into score_mgr

**6. Management commands to load and reset users need unit tests.**

(Yongwen) Create first level class PlayerMgr to:
    * create_user()
    * remove_user()
    * reset_user()
    * load_users()
    * users(type=[admin, RA, normal, eco-rep])

Management commands is a simple wrapper to first level class methods.

**7. Score data (referral bonus, points) directly in model.**

(Yongwen) Could be moved to score_mgr.ScoreMgr.

:mod:`apps.managers.score_mgr`
------------------------------

**8. Does not appear to support definition of new scoring systems (such as 'gallons' for water).**

(Yongwen) Score_mgr currently only handles point management and ranking for
points. Energy ranking is handled in energy_scoreboard widget. Energy
and Water was considered as widget components and un-pluggable.

Ideas:
  * make Energy, Water, Waste as manager components with a common base class, SustainableMgr
  * they all have a similar model, score system, etc. 

**9. Should the score manager have an internal data structure containing the current state of all
scores for all users and teams that is queried by modules?  Or should each player have an instance
of a scoring system that provides their own personal data?**

(Yongwen) The first approach may be less effort with the current model, maybe better performance?

(George) I prefer the idea of each player/team having an instance of a scoring system. Seems more "relational" and cuts down additional database queries.

:mod:`apps.managers.settings_mgr`
---------------------------------

**10. Where should one specify the organizational logo that goes in the header bar?**

(Yongwen) Create a first-level class ChallengeMgr based on Manager class:
  * extends info():  display the challenge details and/or configuration

(George) Logo should be specified in the settings? Seems like it should be placed in the images folder. Maybe just have them put a file named "logo.png" in there?

**11. Should competition_point_label be provided by scoring_mgr?**
**12. Should competition_team_label be provided by team_mgr?**
**13. Should cas_server_url be provided by auth_mgr?**

(Yongwen) They are the user specified settings. The goal is to place them all in
one place for better admin.

Another approach is to provide an interface in the base class Manager
to provide the settings for individual managers and the admin
interface will inspect and aggregate them for user input. Could be
doable.


**14. Lots of settings defined in init.py.  Is this appropriate?**

(Yongwen) Move methods in init.py into first-level class ChallengeMgr. In
general, we could refactor all init.py methods into first-level
classes,  so all methods are class based. same things to views.py
(refactor to class-based view).

(George) Constants and such should be fine in init.py. I've seen constants in there.

**15. The tests.py file does not appear to be invoked during testing.  Is  the indentation wrong?**

(Yongwen) Should be fixed thanks to George. will double check.

:mod:`apps.managers.team_mgr`
-----------------------------

**16. Do we want to hardwire methods to get a particular scoring system (points)?  In the case of
EWC, the "team" will also have a score related to gallons and kWh.**

(Yongwen) Should not need the methods about the point or score. The view layer
could query the score_mgr for such info.


:mod:`apps.widgets.ask_admin`
-----------------------------

**17. The views module hardwires the address for admins.**

(Yongwen) Should be part of the settings. Probably it is better to implement a
common settings interface both for managers and widgets, so that the
admin interface could inspect and aggregate the settings for all.

:mod:`apps.widgets.badges`
--------------------------

**18. Currently we only have three possible badges.  That seems lame; can we think of more?**

(Yongwen) Ten is probably is the minimum. The framework should provide admin
interface to add more:

  * define rules for badge
  * upload badge icon or use default icon

(George) Certainly needs improvement. One idea is to have category badges for the SGG, but it'd have to be generic since the categories are specified by content creators, not us.

:mod:`apps.widgets.energy_goal`
-------------------------------

**19. Should the "manual" energy goal widget be a variant of this module, or
a separate widget (apps.widgets.manual_energy_goal).   Perhaps even
more interestingly, since EWC will have a water challenge, maybe the manual
widget should be able to be instantiated for either water or energy?**

(Yongwen) The current design is to use the energy_goal model to store the data
locally, either from watt depot (via external updater) or manual
input. With Water in the picture, we could create a common goal model
to be extended into energy, water, etc.

(George)  I think the manual energy goal widget should be a configuration option. Although, if the energy goal is looking at a database table for information, does it matter how that table is populated?


**20. It's not really clear how/when energy goal points get awarded.  Is there a
periodic script that gets run each night?  Where is that code? Can we
put it in this module?**

(Yongwen) The award_goal_points methods is for this purpose. There is a nightly
script that simply calls this methods. Need testing.

(George) There is a script that checks. It was bundled in with another script, but that can be moved in here.


:mod:`apps.widgets.energy_power_meter`
--------------------------------------

**21. This widget appears to save energy data locally (as part of the
model).  Is this a change from Makahiki 1? Do we need to be persisting this data, or can we just
keep it in-memory?**

(Yongwen) A redesign from makahiki1. The thought is to remove dependency from
GDATA and run updater to sync data from watt depot. It seems possible
for query watt depot in real time without persistence.


(George) I guess we don't need to persist it. That's what WattDepot is for.


:mod:`apps.widgets.energy_scoreboard`
-------------------------------------

**22. What does the admin interface to this actually accomplish? (Similar question for other energy
widgets?)**

(Yongwen) To support manual data input.

:mod:`apps.widgets.notifications`
---------------------------------

**23. Three functions in init.py.  Can these be moved elsewhere?**

(Yongwen) Could be moved into first-level widget class "NotificationWidget".  Essentially, we will create a first-level class for all widgets
exending from base class "Widget", with the following common
interface:

   * info(): descriptive info for this widget
   * settings(): any settings, both hardwired and user specified.
   * enabled(): user changeable from admin

(George) They should be moved elsewhere if possible.

:mod:`apps.widgets.popular_tasks`
---------------------------------

**24. For consistency with new SGG terminology, should this be "popular_actions"?**

(Yongwen) Yes.

(George) Actions for sure.

:mod:`apps.widgets.prizes`
--------------------------

**25. Should the management command for raffle picking and form printing move to the raffle widget?**

(Yongwen) Yes, it may be enhanced as a admin interface functionality.

(George) Seems reasonable to have raffle related stuff there.

:mod:`apps.widgets.quests`
--------------------------

**26. Should the "utility" functions be in init.py?  More generally, should this module be more object-oriented?**

(Yongwen) Implements the QuestWidget class.

(George) The functions can be moved elsewhere. As for making it more object oriented, maybe? The functions are directly mapped to predicates that are entered in the admin interface. As long as it doesn't cause changes in the way they're entered in the admin interface, I'm okay with it.

:mod:`apps.widgets.scoreboard`
------------------------------

**27. Shouldn't the scoreboard widget refer to the score manager for data?**

(Yongwen) Essentially it already does. The view method could be cleaned up.

:mod:`apps.widgets.smartgrid`
------------------------------

**28. Can this code can be restructured and simplified?  Lots going on in init.py.**

(Yongwen) Yes. Could implement SmartgridWidget and SmartgridView class.

(George)  Definitely needs some cleaning up.

:mod:`apps.widgets.team_members`
---------------------------------

**29. The team_members widget imports player_mgr but nothing from team_mgr.  This seems confusing. Is it correct?**
      
(Yongwen) The code uses team_id directly to query all player objects with the
same team_id.  It may not seem object-oriented by using the db model
directly.

The object-oriented way could be:
1. get the TeamMgr object from player
2. call TeamMgr.members()

There seem to be a good idea to encapsulate the model query, so that
if model changes, only the first-level class implement ion need to be
changed accordingly. The external interface (views, interaction with
other objects) could remain the same.








