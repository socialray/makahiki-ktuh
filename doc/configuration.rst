Configuration
=============

.. note:: When completed, this chapter will discuss: (a) setting the branding, 
          (b) setting the displayed pages and widgets; (c) setting the 
          authentication strategy; (d) configuring individual games (like the 
          DEGG baseline, the SGG contents, the raffle game prizes, the top-scorer
          prizes); (e) specifying round dates; (f) loading the users.


Developing a theme
------------------

Steps:

  * cd to makahiki/static/less
  * copy theme-default.less to a new file named theme-<name>.less
  * edit makahiki/settings.py to add your new theme to INSTALLED_THEMES.
  * set both MAKAHIKI_USE_LESS and MAKAHIKI_DEBUG to True
  * start the server.
  * test your new theme by going to the profile page and changing your theme. 
    Save your changes. you should see your new theme.
  * Edit and save the theme-<name>.less file, then reload the page to see the change.
  * Once happy with the theme compile it using scripts/compile_less.py.   
    The script will compile all the theme-`*`.less files. 
  * Add, Commit and Push the new theme files (.less and .css) and the 
    updated settings.py. 










