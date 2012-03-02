Installation
============

1. Install prerequisite software
--------------------------------

`Python`_ 2.6 or higher (but not Python 3). On Windows machines, it
is recommended that you use the 32 bit version.

`Apple Developer Tools`_ (OS/X only). If on Mac OS X, install
Apple Developer Tools (i.e. XCode 4). This is required in order to 
build certain libraries (PIL, etc.) that require GCC (which is bundled with
XCode).

`Visual C++`_ (Windows only).  If on Windows, you will need to install
Visual Studio.  Please read and follow this `blog post on Django
installation on Windows`_.  Note that Makahiki developers all work on Unix
platforms, so we do not regularly test for Windows compatibility.

`Python Imaging Library`_ (PIL). If you are on OSX, it is easier to
install via `Homebrew`_. Once Homebrew is installed, install PIL by
typing ``brew install pil``. If you are brave enough to install from
source, make sure you have both libjpeg and zlib for jpeg and png
support respectively.

Git. Find a package for your operating system at the `GitHub install
wiki`_. It is recommended that you also configure Git so that it
handles line endings from Windows users correctly. See `Dealing With
Line Endings`_.

Pip. Check if it is installed by typing ``pip help``. If not, install
it by typing ``easy_install pip``. If you do not have easy_install,
download and follow the instructions `here`_.

`Virtualenvwrapper`_. Virtualenv and
Virtualenvwrapper allow you to install libraries separately from your
global Python path. Follow the steps in the introduction and make a
virtualenv for Makahiki (i.e. ``mkvirtualenv makahiki``). You may
also want to define $WORKON\_HOME to your shell startup file in
addition to adding the virtualenv startup script (it uses
``~/.virtualenv`` by default).

`PostgreSQL`_.  Makahiki uses PostgresSQL as its standard backend
database.   Be sure to read the README file; on OS/X you must edit
sysctl.conf in order to ensure that the server runs correctly.  Once
installed, be sure that your PostgreSQL installation's bin/ directory 
is on $PATH so that ``pg_config`` and ``psql`` are defined.  Note for non-Mac users: you
must download postgres-dev in order to get the pg_config command.  It is
important that the user "postgres" is "trusted" so that you can connect to
the server as the user "postgres" locally without authentication.  This should be the
default behavior. 

.. _Python: http://www.python.org/download/
.. _Python Imaging Library: http://www.pythonware.com/products/pil/
.. _Homebrew: http://mxcl.github.com/homebrew/
.. _GitHub install wiki: http://help.github.com/git-installation-redirect
.. _Dealing With Line Endings: http://help.github.com/dealing-with-lineendings/
.. _here: http://pypi.python.org/pypi/setuptools
.. _Virtualenvwrapper: http://www.doughellmann.com/docs/virtualenvwrapper/
.. _PostgreSQL: http://www.postgresql.org/
.. _Apple Developer Tools: https://developer.apple.com/technologies/mac/
.. _Visual C++: http://microsoft.com/visualstudio/en-us/products/2008-editions/express
.. _blog post on Django installation on Windows: http://slacy.com/blog/2011/06/django-postgresql-virtualenv-development-setup-for-windows-7/

2. Download the Makahiki source
-------------------------------

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

3. cd to makahiki, and workon makahiki
--------------------------------------

The remaining steps require you to be in the makahiki directory and to have
activated that virtual environment::

  % cd makahiki/
  % workon makahiki

If you start a new shell in the midst of this process, you must be sure to invoke ``workon makahiki``
and of course cd to the appropriate directory before continuing. 


4. Download and install libraries
---------------------------------

Once you have the source, you must next install a set of third party
libraries into your Makahiki virtual environment::

  % pip install -r requirements.txt
  
This command will produce a lot of output, but it should terminate without
indicating that an error occurred.


5. Configure Postgres database
------------------------------

Next, create a makahiki user and database in your postgres server::

  % scripts/initialize_postgres.py
    CREATE ROLE
    ALTER ROLE
    CREATE DATABASE
    REVOKE
    GRANT
    GRANT


As you can see, executing the script should echo the commands to create the
user and database. 

6. Setup environment variables
------------------------------

Makahiki requires two environment variables: DATABASE_URL and
MAKAHIKI_ADMIN_INFO.  

In Unix, these environment variables can be defined this way::

  % DATABASE_URL=postgres://makahiki:makahiki@localhost:5432/makahiki
  % export DATABASE_URL

  % MAKAHIKI_ADMIN_INFO=admin:admin
  % export MAKAHIKI_ADMIN_INFO

You will want to either add these variables to a login script so they are
always available, or you can edit the postactivate file (in unix, found in
~/.virtualenvs/makahiki/bin) so that they are defined whenever you 
``workon makahiki``.

Note that you will want to provide a stronger password for the makahiki
admin account if this server is publically accessable. 

7.  Configure Postgres database some more
-----------------------------------------

Now you can further configure the postgres database with the models in the
Makahiki system::


  % python manage.py syncdb --noinput
    Syncing...
    Creating tables ...
    Creating table settings_mgr_challengesettings
     :
    Not synced (use migrations):
    - 
   (use ./manage.py migrate to migrate these)

To make sure that the schemas are fully up to date, you invoke the migrate
script::

  % python manage.py migrate

8. Test your installation
-------------------------

To see if the system has been installed correctly, run the tests::

  % python manage.py test

9. Load sample data (optional)
------------------------------

You might want to load some sample data into the system to provide a more
realistic display on login.  If so, do the following::

  % scripts/load_data.sh


10. Bring up the server
-----------------------

Finally, you can start the Makahiki server::

  % python manage.py runserver

Open a browser and go to http://localhost:8000 to see the home page. 


11. Login to administrative interface
-------------------------------------

Once the server is running, you must login as admin in order to continue
configuration. To do this, go to http://localhost:8000/account/login
and login using the credentials you specified in Step (6) above. 

Once you are logged in, go to the administrator page at
http://localhost:8000/admin

(Documentation of page and widget configuration coming soon.)

