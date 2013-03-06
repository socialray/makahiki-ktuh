.. _section-installation-native-windows:

Makahiki Native Windows Installation
====================================

.. WARNING:: Native windows installation should be viewed as "experimental" and should be
   undertaken only by expert Windows developers. 


Install Python
-----------------

`Python`_ 2.7.3 or higher (but not Python 3). It
is recommended that you use the **32 bit** version.

To check that python is installed and has the correct version::

  & python --version
    Python 2.7.3

Install C Compiler
------------------
you will need to install `Visual Studio 2008 Express`_
Please read and follow this `blog post on Django installation on Windows`_.

Install Git
--------------

Find a package for your operating system at the `GitHub install
wiki`_. It is recommended that you also configure Git so that it
handles line endings from Windows users correctly. See `Dealing With
Line Endings`_.

Install Pip
--------------

Download and install the binary "setuptools-0.6c11.win32-py2.7.exe " under the download section of the `setuptools website`_.

Install pip using easy_install::

  %  easy_install pip


Install Virtual Environment Wrapper
-----------------------------------

`Virtualenvwrapper`_ allows you to install libraries separately from your global Python path.

In Windows, you will install `Virtualenvwrapper for Winows`_ which is the port of
`Virtualenvwrapper`_. Follow the "Installation" section to install it in your Windows environment.

Once virtualenv is installed, create a virtual environment for makahiki as follows::

  % mkvirtualenv makahiki


Install Python Imaging Library
---------------------------------

Makahiki requires the `Python Imaging Library`_ (PIL).

You can download and install the pre-build 32bit binary of `PIL for windows`_.

After the PIL is installed, if you want to use the PIL in the virtual environment you just created
in the previous step, you need to copy the PIL package from the system python site-packages to your
virtual environment. For example, if you have created the virtual environment called "makahiki",
copy the directory "C:\\Python27\\Lib\\site-packages\\PIL" to "C:\\Users\\myuser\\Envs\\makahiki\\Lib\\site-packages".
This will make the PIL available in your virtual environment.


Install PostgreSQL
---------------------

Makahiki uses `PostgreSQL`_ as its standard backend database.
Once installed, be sure that your PostgreSQL installation's bin/ directory is on
$PATH so that ``pg_config`` and ``psql`` are defined.

In the development environment, It will be convenient that the user "postgres" is
"trusted" locally so that you can connect to the server as the user "postgres"
locally without authentication. You could edit the
pg_hba.conf file and change "local all postgres ident" to "local all postgres trust".
Or, you may be able to create a .pgpass file containing the credentials. See
PostgreSQL documentation for how to bypass the authentication for localhost.

In the Windows environment, you also need to install the `psycopg2 for windows`_ in order for the python client to use Postgres. You can download the 32bit binary for the corresponding python version and install to your system.

By default, this will install the package into the system python site-packages. If you want to use it in your virtual environment, which is recommended for Makahiki, you will need to copy the directory "C:\\Python27\\Lib\\site-packages\\psycopg2" to the site-packages directory of your virutal environment, for example: "C:\\Users\\myuser\\Envs\\makahiki\\Lib\\site-packages".

.. _Python: http://www.python.org/download/
.. _Python Imaging Library: http://www.pythonware.com/products/pil/
.. _GitHub install wiki: http://help.github.com/git-installation-redirect
.. _Dealing With Line Endings: http://help.github.com/dealing-with-lineendings/
.. _setuptools website: http://pypi.python.org/pypi/setuptools
.. _Virtualenvwrapper: http://www.doughellmann.com/docs/virtualenvwrapper/
.. _Virtualenvwrapper for Winows: http://pypi.python.org/pypi/virtualenvwrapper-win
.. _PostgreSQL: http://www.postgresql.org/
.. _Visual Studio 2008 Express: http://www.microsoft.com/en-us/download/details.aspx?id=14597
.. _blog post on Django installation on Windows: http://slacy.com/blog/2011/06/django-postgresql-virtualenv-development-setup-for-windows-7/
.. _PIL for windows: http://www.pythonware.com/products/pil/PIL-1.1.7.win32-py2.7.exe
.. _psycopg2 for windows: http://www.stickpeople.com/projects/python/win-psycopg/

Download the Makahiki source
---------------------------------

You can download the source by cloning or forking the `Makahiki Git repository`_::

  % git clone git://github.com/csdl/makahiki.git

This will create the new folder and download the code from the repository.

.. _Makahiki Git repository: https://github.com/csdl/makahiki/

Workon makahiki
-------------------

The remaining steps require you to be in the makahiki/ directory and to have
activated that virtual environment::

  % cd makahiki
  % workon makahiki

If you start a new shell in the midst of this process, you must be sure to invoke ``workon makahiki``
and of course cd to the appropriate directory before continuing.

Install required packages
-------------------------
You can install the required Python package for Makahiki by::

  % pip install -r requirements.txt

Setup environment variables
-------------------------------

At a minimum, Makahiki requires two environment variables: MAKAHIKI_DATABASE_URL and
MAKAHIKI_ADMIN_INFO.

In Windows, these environment variables can be defined this way::

  % set MAKAHIKI_DATABASE_URL=postgres://db_user:password@db_host:db_port/db_name

  % set MAKAHIKI_ADMIN_INFO=admin:admin_password

You will want to either add these variables to a login script so they are
always available, or you can edit the ``postactivate`` file in the
``$WORKON_HOME/makahiki/bin`` so that they are defined whenever you
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

  % scripts/initialize_instance.py --type default

This command will:
  * install or update all Python packages required by Makahiki;
  * Reinitialize the database contents and perform any needed database migrations.
  * Initialize the system with data.
  * Set up static files.

.. warning:: Invoke initialize_instance only once!

   The initialize_instance script should be run only a single time in production
   scenarios, because any subsequent configuration will be lost if initialize_instance is
   invoked again.   Use update_instance (discussed below) after performing configuration.


Start the server
--------------------

Finally, you can start the Makahiki server using::

  % ./manage.py runserver

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

5. Finally, restart your server, using::

     % ./manage.py runserver
