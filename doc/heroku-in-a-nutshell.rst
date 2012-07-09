Heroku command line in a nutshell
=================================

This page provides some hints for monitoring a Makahiki application using the heroku
command line. 

Help
----

If you type heroku at the command line without any arguments, it provides simple help::

  % heroku 
  
    Usage: heroku COMMAND [--app APP] [command-specific-options]
  
    Primary help topics, type "heroku help TOPIC" for more details:
  
      addons    # manage addon resources
      apps      # manage apps (create, destroy)
      auth      # authentication (login, logout)
      config    # manage app config vars
      domains   # manage custom domains
      logs      # display logs for an app
      ps        # manage processes (dynos, workers)
      releases  # view release history of an app
      run       # run one-off commands (console, rake)
      sharing   # manage collaborators on an app
  
    Additional topics:
  
      account      # manage heroku account options
      db           # manage the database for an app
      drains       # display syslog drains for an app
      help         # list commands and display help
      keys         # manage authentication keys
      maintenance  # toggle maintenance mode
      pg           # manage heroku postgresql databases
      pgbackups    # manage backups of heroku postgresql databases
      plugins      # manage plugins to the heroku gem
      ssl          # manage ssl certificates for an app
      stack        # manage the stack for an app
      status       # check status of Heroku platform
      update       # update the heroku client
      version      # display version

Logging in
----------

The first time you try to run any command, heroku will request your credentials. For example, let me
invoke the `apps` command::

  % heroku apps
    Authentication failure
    Enter your Heroku credentials.
    Email: johnson@hawaii.edu
    Password: 
    Authentication successful.
    makahiki-hpu
    makahiki-staging-uh
    makahiki-staging-hpu
    makahiki-staging-ewc
    kukuicup-uh
    wattdepot-uh

All of the following commands take a `--app` argument, where you specify the application
of interest. 

Application configuration
-------------------------

To see the environment configuration for your app, run the `config` command with the
application of interest::

  % heroku config --app kukuicup-uh
    DATABASE_URL                     => postgres://blahblah/blah
    FACEBOOKMAKAHIKI_FACEBOOK_APP_ID => 
    LANG                             => en_US.UTF-8
    LD_LIBRARY_PATH                  => /app/.heroku/vendor/lib
    LIBRARY_PATH                     => /app/.heroku/vendor/lib
    MAKAHIKI_ADMIN_INFO              => admin:changeme
    MAKAHIKI_AWS_ACCESS_KEY_ID       => blahblah
    MAKAHIKI_AWS_SECRET_ACCESS_KEY   => blahblah
    MAKAHIKI_AWS_STORAGE_BUCKET_NAME => kukuicup-uh
    MAKAHIKI_EMAIL_INFO              => kukuicup@gmail.com:changeme
    MAKAHIKI_FACEBOOK_APP_ID         => blahblah
    MAKAHIKI_FACEBOOK_SECRET_KEY     => blahblah
    MAKAHIKI_USE_FACEBOOK            => True
    MAKAHIKI_USE_HEROKU              => True
    MAKAHIKI_USE_MEMCACHED           => True
    MAKAHIKI_USE_S3                  => True
    MEMCACHE_PASSWORD                => blah/blah
    MEMCACHE_SERVERS                 => mc6.ec2.northscale.net
    MEMCACHE_USERNAME                => blah%40heroku.com
    PATH                             => /app/.heroku/venv/bin:/bin:/usr/local/bin:/usr/bin
    PYTHONHASHSEED                   => random
    PYTHONHOME                       => /app/.heroku/venv/
    PYTHONPATH                       => /app/
    PYTHONUNBUFFERED                 => true
    SCHEDULER_URL                    => http://blahblah@heroku-scheduler.herokuapp.com/
    SHARED_DATABASE_URL              => postgres://blahblah/blah

Sensitive information has been replaced in the above output.

Running manage.py commands
--------------------------

Use the heroku `run` command to access all of the manage.py commands.  For example, here
is the invocation of the `clear_cache` command to clear the memcache contents::

  % heroku run --app kukuicup-uh makahiki/manage.py clear_cache
    Running makahiki/manage.py clear_cache attached to terminal... up, run.1
    makahiki cache cleared.

See the logs
------------

To see Heroku's command line logging, run the `logs` command::

  % heroku logs --app kukuicup-uh
    2012-06-25T23:12:57+00:00 heroku[router]: GET kukuicup-uh.herokuapp.com/log/level/locked/view-lock-close/ dyno=web.1 queue=0 wait=0ms service=226ms status=200 bytes=5
    2012-06-25T23:15:17+00:00 heroku[api]: Add MAKAHIKI_FACEBOOK_SECRET_KEY, FACEBOOKMAKAHIKI_FACEBOOK_APP_ID, MAKAHIKI_USE_FACEBOOK config by johnson@hawaii.edu
    2012-06-25T23:15:17+00:00 heroku[api]: Release v24 created by johnson@hawaii.edu
    2012-06-25T23:15:17+00:00 heroku[web.1]: State changed from up to bouncing
    2012-06-25T23:15:17+00:00 heroku[web.1]: State changed from bouncing to created
     :
     :

See process status
------------------

Process status is obtained with the `ps` command::

  % heroku ps --app kukuicup-uh
    Process  State      Command                               
    -------  ---------  ------------------------------------  
    web.1    up for 2m  python makahiki/manage.py run_guni..  

To scale an app
---------------

When using a single (free) dyno, Heroku puts your app into an inactive state after some
number of minutes, requiring a few seconds for response to start it up again upon the next
request. 

To prevent this, you must add a dyno (incurring charges).  Here's an example of the command::

  % heroku ps:scale web=2 --app kukuicup-uh

How a collaborator can push a new app
-------------------------------------

The configuration instructions show how you can set up your environment to push out a new
version of the app.   If you are working in a team, then someone else might have done
that for you.  If you later want to push out a new instance to Heroku, the process
is a little different.

First, go to the makahiki directory, workon makahiki, and get the latest version::

  % cd <makahaki directory>  
  % workon makahiki
  % git pull origin master

You may want to run tests to make sure the master is appropriate for pushing to Heroku.

Next, find out what remotes you have already. Make sure the app of interest is not already in
your remotes::

  % git remote -v 
    origin git@github.com:csdl/makahiki.git (fetch)
    origin git@github.com:csdl/makahiki.git (push)


Now add the app of interest (in this case, kukuicup-uh) as a remote::

  % git remote add kukuicup-uh git@heroku.com:kukuicup-uh.git 

Make sure your public keys are available to heroku::

  % heroku keys:add
    Found existing public key: /Users/johnson/.ssh/id_rsa.pub
    Uploading SSH public key /Users/johnson/.ssh/id_rsa.pub

Now invoke the script to push the master to Heroku.  This also updates requirements, syncs the
database, and moves static media to S3::

  % scripts/update_instance.py -r kukuicup-uh
    Counting objects: 15, done.
    Delta compression using up to 4 threads.
    Compressing objects: 100% (3/3), done.
    Writing objects: 100% (9/9), 5.96 KiB, done.
    Total 9 (delta 6), reused 9 (delta 6)

    -----> Heroku receiving push
    -----> Python/Django app detected
    -----> Preparing Python interpreter (2.7.2)
    -----> Creating Virtualenv version 1.7
    New python executable in .heroku/venv/bin/python2.7
    Not overwriting existing python script .heroku/venv/bin/python (you must use .heroku/venv/bin/python2.7)
    Installing distribute.....done.
    Installing pip...............done.
             :
    -----> Noticed pylibmc. Bootstrapping libmemcached.
    -----> Activating virtualenv
    -----> Installing dependencies using pip version 1.0.2
             :
    Cleaning up...
    -----> Installing dj-database-url...
    Cleaning up...
    -----> Injecting Django settings...
    -----> Discovering process types
    -----> Compiled slug size is 26.1MB
    -----> Launching... done, v37

    To git@heroku.com:kukuicup-uh.git
    dec36d4..3313850  master -> master

    Running python makahiki/manage.py syncdb attached to terminal... up, run.1
    Syncing...
    Creating tables ...
    Installing custom SQL ...
    Installing indexes ...
    Installed 0 object(s) from 0 fixture(s)

    Synced:
     > apps.lib.avatar
       :
    Migrated:
    - apps.managers.challenge_mgr
       :












  
 



