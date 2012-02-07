Settings files
==============

settings.py
-----------

This file is the primary settings file Django loads when the system is
running. The other settings are loaded in this script. In development,
the contents of this file may change as new modules are developed.
However, in production, this file should not change unless it is to
remove modules.

makahiki_settings.py
---------------------

This file contains settings specific to this instance of Makahiki. These
include CAS authentication settings, the name of the competition, and
theme settings.

competition_settings.py
------------------------

This file contains settings that are used to specify a particular
competition. Settings include start and end dates for the competition
and round information.
