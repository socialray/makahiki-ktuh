WattDepot Installation (Heroku)
===============================

1. Install Heroku
-----------------

Sign up for an account and install the Heroku toolbelt following
the instructions in the `Heroku Cheat Sheet`_ 

.. _Heroku Cheat Sheet: http://devcenter.heroku.com/articles/quickstart

This involves:
  * Signing up with the Heroku service
  * Install the Heroku Toolbelt (provides the "git" and "heroku" commands).
  * Logging in to Heroku.


2. Download the WattDepot system
--------------------------------

To download the Makahiki system, type the following::

  % git clone git://github.com/csdl/wattdepot.git

This will create a directory called "wattdepot" containing the source code
for the system.

3. Create your Heroku WattDepot application
--------------------------------------------

Change directory to wattdepot, and create the heroku application.  Heroku
requires unique names, so if your organization is "hpu", then you might
call your application "wattdepot-hpu", and get the following output
following these two commands...


