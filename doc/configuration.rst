Configuration and Customization
===============================

.. note:: When completed, this chapter will discuss:

     * The various settings files and how to configure them.
     * How to define the set of game elements in a challenge.
     * How to customize the look-and-feel of the challenge.


System Level Configuration
--------------------------
The "system level configuration" is found in ``settings.py``. This file
configures the database, cache, path, middleware, installed apps and
logging. 

User configuration is limited to  database and cache settings.

.. note:: We probably want to change the default database to postgres, and
          review the remaining settings to see if they are applicable to Makahiki2.

.. include:: ../makahiki/settings.py
   :literal:


Game Level Configuration
------------------------
The configuration for a specific challenge is found in ``game_settings.py``. It is an organization-level configuration, including
the name of the game, competition start/end date, authentication, etc.

.. note:: Should this be called "challenge_settings.py" to avoid ambiguity
          with games? This needs heavy editing for Makahiki2.

.. include:: ../makahiki/game_settings.py
   :literal:


Local Configuration
-------------------
The ``local_settings.py`` contains the secret credentials info and should
not be shared with others, such as check-in to any VCS. It also contains
settings for running tests.

.. note:: This file does not exist.
          

.. include:: ../makahiki/local_settings.py
   :literal:



Page Layout Configuration
-------------------------
This is defined in ``page_settings.py``. It defines the content and layout of all pages in the
system. One can customize this file to create different layouts for a page.

.. include:: ../makahiki/page_settings.py
   :literal:

