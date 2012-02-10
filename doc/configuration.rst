Configuration and Customization
===============================

When complete, this chapter will discuss:
  * The various settings files and how to configure them.
  * How to define the set of game elements in a challenge.
  * How to customize the look-and-feel of the challenge.


System Level Configurations
----------------------------
This is defined in ``settings.py``. The configurations include database, cache, path,
middleware, installed apps and logging. One will mostly like change database and cache settings,
and leave the rests alone.

Game Level Configurations
-------------------------
This is defined in ``game_settings.py``. It is the organization-level configuration, including
the name of the game, competition start/end date, authentication, etc.

Local Configurations
--------------------
The ``local_settings.py`` contains the secret credentials info and should not be shared with others,
such as check-in to any VCS. It also contains settings for running tests.

Page Layout Configuration
-------------------------
This is defined in ``page_settings.py``. It defines the content and layout of all pages in the
system. One can customize this file to create different layouts for a page.

