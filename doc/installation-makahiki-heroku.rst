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


Download the Makahiki source
----------------------------

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

First, you need to define the admin account name and password.  For example::

  % heroku config:add MAKAHIKI_ADMIN_INFO=admin:Dog4Days56

(Add instructions for other environment variables here.)

Initialize Makahiki
-------------------

To initialize your heroku application (for example, "makahiki-hpu") with the default Makahiki data set , invoke the following::

  % cd makahiki
  % scripts/initialize_instance.py -t default -r makahiki-hpu

This command will:
  * Upload the Makahiki source code to Heroku
  * Install and/or update all Python packages required by Makahiki;
  * Reinitialize the database contents and perform any needed database migrations.
  * Initialize the system with data.
  * Set up static files.

If you instead want to create a demo instance to facilitate training or sample use, you can invoke
the initialize_instance script as::

  % scripts/initialize_instance.py -t demo -r makahiki-hpu

This will create a demo instance that enables people to play a simple version of the Kukui
Cup with minimal additional configuration.

.. warning:: Invoke initialize_instance only once!

   The initialize_instance script should be run only a single time in production
   scenarios, because any subsequent configuration will be lost if initialize_instance is
   invoked again.   Use update_instance (discussed below) after performing configuration. 

Start the server
----------------

To start up the server with this configuration, invoke::

  % heroku ps:restart

Verify that Makahiki is running
-------------------------------

Open a browser and go to `http://<heroku-appname>.herokuapp.com/` (where <heroku-appname> is
replaced by your app's name, for example, makahiki-hpu) to see the landing page, which should look like:

.. figure:: figs/guided-tour/guided-tour-landing.png
   :width: 600 px
   :align: center


Configure your Makahiki instance
--------------------------------

Now that you have a running Makahiki instance, it is time to configure it for your
challenge, as documented in :ref:`section-configuration`.

Updating your Makahiki instance
-------------------------------

Makahiki is designed to support post-installation updating of your configured system when bug fixes or
system enhancements become available.   Updating an installed Makahiki instance is quite
simple, and consists of the following steps.

1. Get the updated source code::

   % git pull origin master

3. Run the update_instance script to update your Heroku configuration::

   % cd makahiki
   % scripts/update_instance.py -r makahiki-hpu

4. Finally, restart your server::

     % heroku ps:restart






