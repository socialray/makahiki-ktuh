Heroku installation of Makahiki
===============================

Install Heroku
--------------

Sign up for an account and install the Heroku toolbelt following
the instructions in the `Heroku Cheat Sheet`_ 

.. _Heroku Cheat Sheet: http://devcenter.heroku.com/articles/quickstart

This involves:
  * Signing up with the Heroku service
  * Install the Heroku Toolbelt (provides the "git" and "heroku" commands).
  * Logging in to Heroku.


Setup Amazon S3
---------------
In order to use Heroku with Makahiki, and because Heroku does not host static files, you will need to set up the Amazon S3 for serving the static files in Makahiki heroku instance.

Follow `Using AWS S3 to store static assets <https://devcenter.heroku.com/articles/s3>`_ for details to setup the Amazon S3.

Create a S3 bucket to be used for storing the static files for Makahiki, and record the bucket name you created, the AWW access key id, and the AWS secret access key for use in setting up the environment variables for Heroku.

Download the Makahiki source
----------------------------

To download the Makahiki system, type the following::

  % git clone git://github.com/csdl/makahiki.git

This will create a directory called "makahiki" containing the source code
for the system.

Setup environment variables
---------------------------

Makahiki requires several environment variables to be set.

First, you need to define the admin account name and password.  For example::

  % export MAKAHIKI_ADMIN_INFO=admin:Dog4Days56

You will also need to define the Amazon S3 information in the following environment variables::

  % export MAKAHIKI_AWS_ACCESS_KEY_ID=<AWS access key id>
  % export MAKAHIKI_AWS_SECRET_ACCESS_KEY=<AWS secret access key>
  % export MAKAHIKI_AWS_STORAGE_BUCKET_NAME=<AWS S3 bucket name>

They are the information you gathered from the previous step.

Initialize Makahiki
-------------------

Once the environment variables are setup, you can create a heroku application and initialize the application with the default Makahiki data set. Heroku application name need to be unique as required by Heroku, so if your organization is "hpu", then you might
call your application "makahiki-hpu". Use an application name appropriate for your organization.

To initialize your heroku application (for example, "makahiki-hpu") with the default Makahiki data set , invoke the following::

  % cd makahiki
  % scripts/initialize_instance.py -t default -r makahiki-hpu

This command will:
  * create the application in Heroku
  * install necessary Heroku addons
  * set up the Makahiki environments you defined for the application
  * Upload the Makahiki source code to Heroku
  * Install and/or update all Python packages required by Makahiki
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

  % heroku ps:restart -a makahiki-hpu

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
challenge, as documented in :ref:`section-site-configuration`.

Updating your Makahiki instance
-------------------------------

Makahiki is designed to support post-installation updating of your configured system when bug fixes or
system enhancements become available.   Updating an installed Makahiki instance is quite
simple, and consists of the following steps.

#. Get the updated source code::

   % git pull origin master

#. Run the update_instance script to update your Heroku configuration (make sure the AWS environment variables are set)::

   % cd makahiki
   % scripts/update_instance.py -r makahiki-hpu

#. Finally, restart your server::

     % heroku ps:restart






