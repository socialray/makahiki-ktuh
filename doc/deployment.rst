Deployment
==========

When complete, this chapter will discuss:
  * How to bring up a local instance of a configured system for testing and evaluation.
  * How to create a production deployment to local hardware.
  * How to create a production deployment using Heroku.
  * How to perform load-testing to ensure that the system is adequately responsive.

Deploy to Heroku
----------------

First, we create a heroku app and a git remote on the working space.

``heroku create --stack cedar --remote heroku``

It should say "Git remote heroku added" at the end of the output.

``git push heroku master''

It should say it pushed to ``git@heroku.com:<our-heroku-app>.git``
now you can check the status of your app by running:

``heroku ps``

The output should show "State" as "up".

To see the app's console log, run:

``heroku logs``

Now we can syncdb and load data into the app by running a local script:

``deploy/heroku_deploy.sh``

That is it. The app is available at ``http://<our-heroku-app>.herokuapp.com/``.