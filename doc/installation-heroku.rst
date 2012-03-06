Makahiki Installation (Heroku)
==============================

1. Install Heroku
-----------------

Sign up for an account and install the Heroku toolbelt following
the instructions in the `Heroku Cheat Sheet`_ 

.. _Heroku Cheat Sheet: http://devcenter.heroku.com/articles/quickstart

This involves:
  * Signing up with the Heroku service
  * Install the Heroku Toolbelt (provides the "git" and "heroku" commands).
  * Logging in to Heroku.


2. Download the Makahiki system
-------------------------------

To download the Makahiki system, type the following::

  % git clone git://github.com/csdl/makahiki.git

This will create a directory called "makahiki" containing the source code
for the system.

3. Create your Heroku Makahiki application
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

4. Define a Makahiki admin account and password
-----------------------------------------------

Now tell Heroku the administrator account name and its password.  Choose a
password that is not easily guessed and is different from that shown
below. You can also choose a different admin account name if you wish::

  % heroku config:add MAKAHIKI_ADMIN_INFO=admin:Dog4Days56

5. Send the Makahiki system to Heroku
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


6. Configure the Heroku installation of Makahiki
------------------------------------------------

A few final commands are needed to get your Makahiki application running on Heroku::

  % heroku run python makahiki/manage.py syncdb --noinput
  % heroku run python makahiki/manage.py migrate
  % heroku open

This last command should bring up a browser and retrieve the home page of
your Makahiki application running on Heroku.


7. Login to administrative interface
-------------------------------------

Once the server is running, you must login as admin in order to continue
configuration. To do this, go to http://localhost:8000/account/login
and login using the credentials you specified in Step (6) above. 

Once you are logged in, go to the administrator page at
http://localhost:8000/admin

(Documentation of page and widget configuration coming soon.)

