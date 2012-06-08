Makahiki Installation (Heroku)
==============================

Install Heroku
-----------------

Sign up for an account and install the Heroku toolbelt following
the instructions in the `Heroku Cheat Sheet`_ 

.. _Heroku Cheat Sheet: http://devcenter.heroku.com/articles/quickstart

This involves:
  * Signing up with the Heroku service
  * Install the Heroku Toolbelt (provides the "git" and "heroku" commands).
  * Logging in to Heroku.


Download the Makahiki system
-------------------------------

To download the Makahiki system, type the following::

  % git clone git://github.com/csdl/makahiki.git

This will create a directory called "makahiki" containing the source code
for the system.

Create your Heroku Makahiki application
------------------------------------------

Change directory to makahiki, and create the heroku application.  Heroku
requires unique names, so if your organization is "hpu", then you might
call your application "makahiki-hpu", and get the following output
following these two commands::

  % cd makahiki
  % heroku create makahiki-hpu --stack cedar --remote heroku
    Creating makahiki-hpu... done, stack is cedar
    http://makahiki-hpu.herokuapp.com/ | git@heroku.com:makahiki-hpu.git
    Git remote heroku added

Use an application name appropriate for your organization.

Setup environment variables
---------------------------

Makahiki requires several environment variables to be set.

First, you need to define the admin account name and password.  For example:

  % heroku config:add MAKAHIKI_ADMIN_INFO=admin:Dog4Days56

(Add instructions for other environment variables here.)

Send the Makahiki system to Heroku
-------------------------------------

To upload the Makahiki source code to Heroku, do the following::

  % git push heroku master

This will result in a lot of output, ending with the following if all goes
well::

    Cleaning up...
    -----> Injecting Django settings...
           Injecting code into makahiki/settings.py to read from DATABASE_URL
    -----> Discovering process types
           Procfile declares types -> web
    -----> Compiled slug size is 14.9MB
    -----> Launching... done, v5
           http://makahiki-hpu.herokuapp.com deployed to Heroku

    To git@heroku.com:makahiki-hpu.git
    * [new branch]      master -> master


Initialize Makahiki
-------------------

To initialize your Makahiki instance with the default data set, invoke the following::

  % heroku run python scripts/initialize_instance.py -t default

When deploying to Heroku, the "default" Makahiki configuration is normally the only one you will
want to use. 

Start the server
----------------

To start up the server with this configuration, invoke::

  % heroku ps:restart

Verify that Makahiki is running
-------------------------------

Open a browser and go to http://<heroku-appname>.herokuapp.com/ (where <heroku-appname> is
replaced by your app's name) to see the landing page, which should look like:

.. figure:: figs/guided-tour/landing.png
   :width: 600 px
   :align: center


Configure your Makahiki instance
--------------------------------

Now that you have a running Makahiki instance, it is time to configure it for your
challenge, as documented in :ref:`section-configuration`.





