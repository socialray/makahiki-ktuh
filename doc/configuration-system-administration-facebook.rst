.. _section-configuration-system-administration-facebook:

Configure Facebook integration (Optional)
=========================================

About Facebook integration
--------------------------

Makahiki currently integrates with facebook in the following ways:

  1. you can request that your Facebook photo be used as your Makahiki profile picture,

  2. you are given an oppportunity to post to Facebook when the system notifies you of an accomplishment.

To enable the above Facebook integration in Makahiki, the system admin will need to create an Facebook app and configure the app information in Makahiki, as described in the next section.

Configuring Facebook integration
--------------------------------

First you will need to create a Facebook app at:
https://developers.facebook.com/apps

After you created your app, say, "makahiki-app", click on the "Website with Faceook Login" setting, enter the URL of your server, for instance, http://localhost:8000, in the "Site URL" field, then click on the "Save Changes" button.

You should see the "App ID" and "App Secret" value of your app under the app name.

Now, you can set the following environment variables to enable facebook integration::

    % export MAKAHIKI_USE_FACEBOOK=True
    % export MAKAHIKI_FACEBOOK_APP_ID=<your_app_id>
    % export MAKAHIKI_FACEBOOK_SECRET_KEY=<your_app_secret_key>

On Heroku, you can set the environment variable using::

  % heroku config:add <ENV_KEY>=<ENV_VALUE>

Last, you need to restart the Makahiki server.

If you want to turn off the Facebook integration, you can set the envrionment variable MAKAHIKI_USE_FACEBOOK=False and restart the server.