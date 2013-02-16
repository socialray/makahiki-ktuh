.. _section-environment-variables:

Environment Variables
=====================

The page provides a reference guide to the environment variables. 

.. note::  This environment variable documentation is extracted autogmatically from the
           settings.py file.  For this reason, the documentation shows the string
           "settings." on the front of each environment variable name.  The actual
           environment variable name is the uppercase string without the "settings." prefix.

.. note::  To set the environment variables in a local installation, use OS specific commands.
           For example, in Unix bash, to set the environment variable MAKAHIKI_EMAIL_INFO::

           % export MAKAHIKI_EMAIL_INFO=kukuicup@changeme.com:changeme

           To set it in the heroku installation, use the heroku config:add command.
           For example::

           % heroku config:add MAKAHIKI_EMAIL_INFO=kukuicup@changeme.com:changeme

.. automodule:: settings
   :members:
   :member-order: bysource






