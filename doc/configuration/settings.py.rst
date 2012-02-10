System Configuration Settings
=============================

The "system level configuration" is found in ``settings.py``. This file
configures the database, cache, path, middleware, installed apps and
logging. 

User configuration is limited to  database and cache settings.

.. note:: We probably want to change the default database to postgres, and
          review the remaining settings to see if they are applicable to
          Makahiki2.  Maybe move the user-configurable stuff up to the top
          of the file? 
 

.. include:: ../../makahiki/settings.py
   :literal:
