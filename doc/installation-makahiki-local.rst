.. _section-installation-makahiki-local:

Makahiki Installation (Local)
=============================

Note that these instructions have only been tested on Mac OS X and Linux. The
Makahiki developers all work on Unix platforms, so we do not regularly test for
Windows compatibility. When we are aware of special steps required for Windows,
they have been noted below.

These instructions also assume that you are using a Bourne-type shell (such as
bash), which is the default on Mac OS X and Linux. Using a C-shell variant
(like tcsh), is possible but not recommended.

Hardware requirements 
---------------------

Our estimated hardware requirements (for production use) are:
  * CPU:  modern dual or quad core
  * RAM: 8 GB
  * Disk space: 10 GB

Install Python
-----------------

`Python`_ 2.7.1 or higher (but not Python 3). On Windows machines, it
is recommended that you use the 32 bit version.

To check that python is installed and has the correct version::

  & python --version 
    Python 2.7.1

Install C++
--------------

Mac OS X: Install Apple Developer Tools
*******************************************


If you are using Mac OS X, install
`Apple Developer Tools`_ (i.e. Xcode 4). This is required in order to 
build certain libraries (PIL, etc.) that require GCC (which is bundled with
Xcode). Xcode can either be found in your OS X installation DVD, or in the Mac
App Store.

Windows: Install Visual C++
*******************************

If on Windows, you will need to install `Visual C++`_ 
Please read and follow this `blog post on Django installation on Windows`_.

Install Python Imaging Library
---------------------------------

Makahiki requires the `Python Imaging Library`_ (PIL). If you are on Mac OS X, we have found 
`Homebrew`_ to be the most reliable way to install PIL. 
Once Homebrew is installed, install PIL by typing::

  % brew install pil 

If you are brave enough to install from source, make sure you have both libjpeg (for JPEG)
and zlib (for PNG). On Linux, a developer has reported that the PIL system installed by
apt-get does not support JPEG (April, 2012).  To fix, the developer downloaded and
installed from source.

Install Git
--------------

Find a package for your operating system at the `GitHub install
wiki`_. It is recommended that you also configure Git so that it
handles line endings from Windows users correctly. See `Dealing With
Line Endings`_.

Install Pip
--------------

Install it by typing::

  %  easy_install pip

Depending on your system configuration, you may
have to type ``sudo easy_install pip``. If you do not have easy_install,
download and install it from the `setuptools website`_.

Install Virtual Environment Wrapper
---------------------------------------

`Virtualenvwrapper`_ allows you to install
libraries separately from your global Python path. Follow the
`virtualenvwrapper installation instructions`_ through the Quick Start section.

Once virtualenv is installed, create a virtual environment for makahiki as follows::


  % mkvirtualenv makahiki

Install PostgreSQL
---------------------

Makahiki uses `PostgreSQL`_ as its standard backend database.
Note that on Mac OS X, the installer will need to make changes in the
``sysctl`` settings and a reboot before installation can proceed. Once
installed, be sure that your PostgreSQL installation's bin/ directory is on
$PATH so that ``pg_config`` and ``psql`` are defined.  

.. note:: For Linux users: you must download postgres-dev in order to get the pg_config
          command. It is important that the user "postgres" is "trusted" so that you can
          connect to the server as the user "postgres" locally without authentication. If
          that is not the case, you must edit the pg_hba.conf file and change "local all
          postgres ident" to "local all postgres trust". Or, you may be able to create a
          .pgpass file containing the credentials.

Install Memcache
-------------------

Makahiki can optionally use `Memcache`_ to improve performance.
To avoid the need for alternative configuration files, we require local installations to install
Memcache and an associated library even if they aren't intending to use it.  On Mac OS X,
if you have installed `Homebrew`_, you can install these by typing::

  % brew install memcached
  % brew install libmemcached

For other environments, one place to start is `Heroku's memcache
installation instructions`_, although these instructions do not explain installation of libmemcached.

.. _Python: http://www.python.org/download/
.. _Python Imaging Library: http://www.pythonware.com/products/pil/
.. _Homebrew: http://mxcl.github.com/homebrew/
.. _GitHub install wiki: http://help.github.com/git-installation-redirect
.. _Dealing With Line Endings: http://help.github.com/dealing-with-lineendings/
.. _setuptools website: http://pypi.python.org/pypi/setuptools
.. _Virtualenvwrapper: http://www.doughellmann.com/docs/virtualenvwrapper/
.. _virtualenvwrapper installation instructions: http://www.doughellmann.com/docs/virtualenvwrapper/install.html#basic-installation
.. _PostgreSQL: http://www.postgresql.org/
.. _Apple Developer Tools: https://developer.apple.com/technologies/mac/
.. _Visual C++: http://microsoft.com/visualstudio/en-us/products/2008-editions/express
.. _blog post on Django installation on Windows: http://slacy.com/blog/2011/06/django-postgresql-virtualenv-development-setup-for-windows-7/
.. _Memcache: http://memcached.org
.. _Heroku's memcache installation instructions: http://devcenter.heroku.com/articles/memcache#local_memcache_setup

Download the Makahiki source
---------------------------------

To download the source for your own fork::

  % git clone git://github.com/csdl/makahiki.git

If you wish to commit to the Makahiki project, you will need to
create an account at `GitHub`_. Then, you will need to set up your
`SSH keys`_ and your `email settings`_.

Once those are set up, send a Makahiki developer your Git username so that you can be
added as a collaborator.

Once you are added as a collaborator, you should be able to check out the
code as follows::

  % git clone git@github.com:csdl/makahiki.git

This will create the new folder and download the code from the repository.

.. _GitHub: http://github.com
.. _SSH keys: http://help.github.com/key-setup-redirect
.. _email settings: http://help.github.com/git-email-settings/

Workon makahiki
-------------------

The remaining steps require you to be in the makahiki/ directory and to have
activated that virtual environment::

  % cd makahiki/
  % workon makahiki

If you start a new shell in the midst of this process, you must be sure to invoke ``workon makahiki``
and of course cd to the appropriate directory before continuing. 

Setup environment variables
-------------------------------

At a minimum, Makahiki requires two environment variables: MAKAHIKI_DATABASE_URL and
MAKAHIKI_ADMIN_INFO.  

In Unix, these environment variables can be defined this way::

  % export MAKAHIKI_DATABASE_URL=postgres://db_user:password@db_host:db_port/db_name

  % export MAKAHIKI_ADMIN_INFO=admin:admin_password

You will want to either add these variables to a login script so they are
always available, or you can edit the ``postactivate`` file (in Unix, found in
``$WORKON_HOME/makahiki/bin``) so that they are defined whenever you 
``workon makahiki``.

Note that you will want to provide a stronger password for the makahiki
admin account if this server is publically accessible. 

Makahiki also utilizes a variety of other environment variables. For complete
documentation, see :ref:`section-environment-variables`.

Initialize Makahiki
-------------------

Next, invoke the initialize_instance script, passing it an argument to specify what kind
of initial data to load.  In most cases, you will want to load the default dataset, as
shown next::

  % scripts/initialize_instance.py -t default

This command will:
  * Install and/or update all Python packages required by Makahiki;
  * Reinitialize the database contents and perform any needed database migrations. 
  * Initialize the system with data.
  * Set up static files. 

If you instead want to create a demo instance to facilitate training or sample use, you can invoke
the initialize_instance script as::

  % scripts/initialize_instance.py -t demo

This will create a demo instance that enables people to play a simple version of the Kukui
Cup with minimal additional configuration.

.. warning:: Invoke initialize_instance only once!

   The initialize_instance script should be run only a single time in production
   scenarios, because any subsequent configuration will be lost if initialize_instance is
   invoked again.   Use update_instance (discussed below) after performing configuration. 


Start the server
--------------------

Finally, you can start the Makahiki server using either::

  % ./manage.py run_gunicorn

or::

  % ./manage.py runserver

The first alternative (run_gunicorn) runs a more efficient web server, while the second (runserver) invokes a server
that is better for development (for example, :ref:`section-theme-development`).

Verify that Makahiki is running
-------------------------------

Open a browser and go to http://localhost:8000 to see the landing page, which should look
something like this:

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

1. Bring down the running server in the shell process running Makahiki::

   % (type control-c in the shell running the makahiki server process)
 
2. In that shell or a new shell, go to your Makahiki installation directory, and ensure
   the Makahiki virtual environment is set up::

   % cd makahiki
   % workon makahiki

3. Download the updated source code into your Makahiki installation::

   % git pull origin master

4. Run the update_instance script to update your local configuration::

   % ./scripts/update_instance.py

5. Finally, restart your server, using either::

     % ./manage.py run_gunicorn

   or::

     % ./manage.py runserver



