.. _section-installation-makahiki-local-unix:

Local installation on Unix
==========================

These instructions also assume that you are using a Bourne-type shell (such as bash),
which is the default on Mac OS X and Linux. Using a C-shell variant
(like tcsh), is possible but not recommended.

Hardware requirements
---------------------

Our estimated hardware requirements for **production** use are:
  * CPU:  modern dual or quad core
  * RAM: 8 GB
  * Disk space: 10 GB

For **development** only, a modern dual core CPU with 4 GB should be ok, although the more the better.

Install Python
--------------

`Python`_ 2.7.3 or higher (but not Python 3).

To check that python is installed and has the correct version::

  % python --version 
    Python 2.7.3

Install C Compiler
------------------

If you are using Mac OS X, install
`Apple Developer Tools`_ (i.e. Xcode 4). This is required in order to 
build certain libraries (PIL, etc.) that require GCC (which is bundled with
Xcode). Xcode can either be found in your OS X installation DVD, or in the Mac
App Store.

If on Linux, in most cases, you will find the C/C++ compiler is already installed in your environment.

To check that C compiler is installed::

  % gcc --version 


Install Git
-----------

Find a package for your operating system at the `GitHub install
wiki`_. We recommend following the GitHub setup instructions at https://help.github.com/articles/set-up-git.

To check that Git is installed::

  % git --version 


Install Pip
-----------

Install it by typing::

  % easy_install pip

Depending on your system configuration, you may
have to type ``sudo easy_install pip``. If you do not have easy_install,
download and install it from the `setuptools website`_. Linux (Ubuntu) users can use 
``sudo apt-get install python-setuptools``.

To check that Pip is installed::

  % pip --version 

Install Virtual Environment Wrapper
-----------------------------------

`Virtualenvwrapper`_ allows you to install libraries separately from your global Python path.

Follow the `virtualenvwrapper installation instructions`_ through the Quick Start section to install virtualenv and virtualenvwrapper. Once they are installed, create a virtual environment for makahiki as follows::

  % mkvirtualenv makahiki

To check that virtual environment wrapper is installed::

  % workon makahiki

Install Python Imaging Library
------------------------------

Makahiki requires the `Python Imaging Library`_ (PIL).

Mac OS X
********

we have found `Homebrew`_ to be the most reliable way to install PIL.
Once Homebrew is installed, install PIL by typing::

  % brew install pil

Linux
*****

In Ubuntu, install PIL by typing::

  % sudo apt-get install -y python-imaging python-dev libjpeg-dev

Make sure you have both libjpeg (for JPEG) and zlib (for PNG) in the /usr/lib directory. If not, you can make the symbolic link there. For example, in a 32bit OS, do the following::

  % sudo ln -s /usr/lib/i386-linux-gnu/libjpeg.so /usr/lib/
  % sudo ln -s /usr/lib/i386-linux-gnu/libz.so /usr/lib/


Install PostgreSQL
------------------

Makahiki uses `PostgreSQL`_ as its standard backend database. We recommend version 9.1.3.
Note that on Mac OS X, the installer will need to make changes in the
``sysctl`` settings and a reboot before installation can proceed. Once
installed, be sure that your PostgreSQL installation's bin/ directory is on
$PATH so that ``pg_config`` and ``psql`` are defined.

You will also need to configure authentication for the "postgres" database user.   

During development, a simple way to configure authentication is to make the postgres user
"trusted" locally.  This means that local processes such as Makahiki can connect to the
database server as the user postgres without authentication. To configure this way, edit
the pg_hba.conf file and change::

  local all postgres ident

to:: 

  local all postgres trust

The first line might be: "local all postgres peer". Change it to "local all postgres trust". If
you update the pg_hba.conf file you will have to restart the postgres server. For Linux use::

  % /etc/init.d/postgresql restart

or::

  % sudo /etc/init.d/postgresql restart

Alternatively, you can create a .pgpass file containing the credentials for the user postgres. See
the PostgreSQL documentation for more information on the .pgpass file.

Linux users need to install the ``libpq-dev`` package using ``sudo apt-get install libpq-dev``.

To check that PostgresSQL is installed and configured with "trusted" locally::

  % psql -U postgres

It should not prompt you for password.


Install Memcache
----------------

Makahiki can optionally use `Memcache`_ to improve performance, especially in the
production environment.  To avoid the need for alternative configuration files, we require
local installations to install Memcache and an associated library even if developers aren't
intending to use it.

Mac OS X
********
On Mac OS X, if you have installed `Homebrew`_, you can install these by typing::

  % brew install memcached
  % brew install libmemcached

Linux
*****
For Ubuntu, install memcached as follows::

  % sudo apt-get install memcached
  % sudo apt-get install libmemcached-dev


.. _Python: http://www.python.org/download/
.. _Python Imaging Library: http://www.pythonware.com/products/pil/
.. _Homebrew: http://mxcl.github.com/homebrew/
.. _GitHub install wiki: http://help.github.com/git-installation-redirect
.. _setuptools website: http://pypi.python.org/pypi/setuptools
.. _Virtualenvwrapper: http://www.doughellmann.com/docs/virtualenvwrapper/
.. _virtualenvwrapper installation instructions: http://www.doughellmann.com/docs/virtualenvwrapper/install.html#basic-installation
.. _PostgreSQL: http://www.postgresql.org/
.. _Apple Developer Tools: https://developer.apple.com/technologies/mac/
.. _Memcache: http://memcached.org
.. _Heroku's memcache installation instructions: http://devcenter.heroku.com/articles/memcache#local_memcache_setup

Download the Makahiki source
----------------------------

You can download the source by cloning or forking the `Makahiki Git repository`_::

  % git clone git://github.com/csdl/makahiki.git

This will create the new folder and download the code from the repository.

.. _Makahiki Git repository: https://github.com/csdl/makahiki/

Workon makahiki
---------------

The remaining steps require you to be in the makahiki/ directory and to have
activated that virtual environment::

  % cd makahiki/
  % workon makahiki

If you start a new shell in the midst of this process, you must be sure to invoke ``workon makahiki``
and of course cd to the appropriate directory before continuing. 

Install required packages
-------------------------

You can install the required Python package for Makahiki by::

  % pip install -r requirements.txt

Don't worry that this command generates lots and lots of output.

Setup environment variables
---------------------------

At a minimum, Makahiki requires two environment variables: MAKAHIKI_DATABASE_URL and
MAKAHIKI_ADMIN_INFO.  

The following lines show example settings for these two environment variables, preceded by 
a comment line describing their syntax::

  % # Syntax: postgres://<db_user>:<db_password>@<db_host>:<db_port>/<db_name>
  % export MAKAHIKI_DATABASE_URL=postgres://makahiki:makahiki@localhost:5432/makahiki

  % # Syntax:  <admin_name>:<admin_password>
  % export MAKAHIKI_ADMIN_INFO=admin:admin

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
of initial data to load. You need to be in the makahiki/makahiki directory. In most cases, 
you will want to load the default dataset, as shown next::

  % cd makahiki
  % scripts/initialize_instance.py --type default

This command will:
  * Install and/or update all Python packages required by Makahiki;
  * Reinitialize the database contents and perform any needed database migrations. 
  * Initialize the system with data.
  * Set up static files. 

.. warning:: initialize_instance will wipe out all challenge configuration modifications!

   The initialize_instance script should be run only a single time in production
   scenarios, because any subsequent configuration modifications will be lost if initialize_instance is
   invoked again.   Use update_instance (discussed below) to update source code without
   losing subsequent configuration actions.

You will have to answer 'Y' to the question "Do you wish to continue (Y/n)?"
 
Start the server
----------------

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
challenge, as documented in :ref:`section-site-configuration`.

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



