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

To deploy Makahiki on Heroku, you must define several local environment variables that will be
used by the initialize_instance script when it configures the Heroku instance.

First, define a local environment variable that specifies the Heroku Makahiki admin account name and
password::


  % export MAKAHIKI_ADMIN_INFO=admin:Dog4Days56

You will also need to define Amazon S3 information::

  % export MAKAHIKI_AWS_ACCESS_KEY_ID=<AWS access key id>
  % export MAKAHIKI_AWS_SECRET_ACCESS_KEY=<AWS secret access key>
  % export MAKAHIKI_AWS_STORAGE_BUCKET_NAME=<AWS S3 bucket name>

You will have obtained these values in the previous section.

Initialize Makahiki
-------------------

Once the above local environment variables are set, you can use the initialize_instance
script to create a Heroku application
and initialize the application with the default Makahiki data set. All Heroku application
names must be unique, so if your organization is "hpu", then you might call your
application "makahiki-hpu". Use an application name appropriate for your organization.

To initialize your heroku application (for example, "makahiki-hpu") with the default Makahiki data set, invoke the following::

  % cd makahiki
  % scripts/initialize_instance.py --type default --heroku makahiki-hpu

This command will:
  * create the application in Heroku
  * install necessary Heroku addons such as memcache
  * set up the Makahiki environments you defined for the application
  * upload the Makahiki source code to Heroku
  * install and/or update all Python packages required by Makahiki
  * initialize the database contents and perform any needed database migrations.
  * initialize the system with data.
  * set up static files.

.. warning:: initialize_instance will delete any Makahiki challenge configuration actions!

   The initialize_instance script should be run only a single time in production
   scenarios, because any subsequent challenge configuration will be lost if initialize_instance is
   invoked again.   Instead, use update_instance (discussed below) after performing configuration. 

Start the server
----------------

To start up the server on Heroku, invoke::

  % heroku ps:restart -a makahiki-hpu

Verify that Makahiki is running
-------------------------------

Open a browser and go to `http://<heroku-appname>.herokuapp.com/` (where <heroku-appname> is
replaced by your app's name, for example, makahiki-hpu).  This should retrieve the landing page, which should look like:

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






