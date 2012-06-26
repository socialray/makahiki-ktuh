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











  
 



