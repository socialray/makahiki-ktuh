.. _section-hello-world-widget-development:
 
Hello World Widget Development
==============================

This quick tutorial demonstrates how to create a simple Hello World widget for Makahiki.

The following sections provide a step by step guide to developing a new widget for Makahiki.  These
sections document the actual steps taken to develop the Hello World Widget.


Create a local installation
---------------------------

The first step in theme development is to follow the local installation guide to create a
running implementation on your computer, as documented in
:ref:`section-installation-makahiki-local`.

Set environment variables for theme development
-----------------------------------------------

To simplify theme development, it is important to set the MAKAHIKI_USE_LESS and
MAKAHIKI_DEBUG environment variables to true.  When this is done, you can make changes to
your theme file, save it, and then simply refresh the page to see the changes. 

There are a variety of ways to set these environment variables, but a convenient way is to
set them in the ~/.virtualenvs/makahiki/bin/postactivate file.   This way, whenever you
`workon makahiki`, the variables will be set.   Here, for example, is the contents of my
postactivate file::

  #!/bin/bash
  # This hook is run after this virtualenv is activated.

  MAKAHIKI_DATABASE_URL=postgres://makahiki:makahiki@localhost:5432/makahiki
  export MAKAHIKI_DATABASE_URL

  MAKAHIKI_ADMIN_INFO=admin:admin
  export MAKAHIKI_ADMIN_INFO

  MAKAHIKI_USE_LESS=True
  export MAKAHIKI_USE_LESS

  MAKAHIKI_DEBUG=True
  export MAKAHIKI_DEBUG

Once you have edited this file, you will need to `workon makahiki` again to set these
variables.  To verify they are set correctly, you can do the following::

  % printenv | grep MAKAHIKI
  MAKAHIKI_DEBUG=True
  MAKAHIKI_DATABASE_URL=postgres://makahiki:makahiki@localhost:5432/makahiki
  MAKAHIKI_ADMIN_INFO=admin:admin
  MAKAHIKI_USE_LESS=True

Create the hello world widget package
-------------------------------------

The first step to create the hello_world widget is to create the new
PyDev package. 

* In eclipse right click on apps/widgets and select "New, PyDev
  Package", type the name "hello_world" in the dialog box and press
  finish.

* Create the ``templates`` directory. This directory will hold the
  template that defines the view for our widget. By Makahiki
  convention the widget's base page is named ``index.html``.

* All Makahiki widgets must have a ``views.py`` file to supply the
  data for the Django template user interface, so create it also.
  We'll discuss the contents of this file a little bit later.

The widget's package should look like::

  hello_world/
              templates/
                        index.html
              __init__.py
              views.py


``__init__.py`` describes the purpose of the widget. Here's the contents for our widget.::

  """The hello_world widget provides an simple example Makahiki widget showing
  player's name, team and current point total."""

We'll go through contents each of the rest of the files next.

The Widget's User Interface ``index.html``
------------------------------------------

Makahiki uses Django templates for the User Interface for widgets.
Let's build a simple UI for our Hello World widget.  Since we are
going to put our widget in an existing page, the widget only needs
enough ``html`` to show itself.

Makahiki provides many different styles and CSS classes.  Here is
template for our Hello World widget::

  <div class="content-box">
        <div class="content-box-title">
            Hello World
            <a href="#" style="float: right">
                <img src="{{ STATIC_URL}}images/icons/icon-help-sm.png" width="20"
                     align="center"
                     title="Click to get help about this window"
                     onclick="toggleHelp(event, 'widget', 'hello-world'); return false;" />
            </a>
        </div>
        <div class="content-box-contents">
            Hello <em>{{ view_objects.hello_world.name }}</em>, you're in team 
            <em>{{ view_objects.hello_world.team }}</em> and have 
            <em>{{ view_objects.hello_world.points}}</em> points.
        </div> 
  </div>

Notice the outter ``content-box``, this provides a rounded, shadowed
box for our widget.  The ``content-box-title`` gives us a highlighted
title and a help icon that will pop-up a help dialog box.  The
``content-box-contents`` div is the main body of our widget.  We get
the player's name, team, and points from the Django template.

Providing data to the UI ``views.py``
-----------------------------------------

Makahiki has a standard way of getting data to the widgets:

* When the player/user loads a page the ``apps.pages.views.index``
  function is called. The ``index`` function determines the name of
  the page and creates a dictionary of ``view_objects``, then calls
  ``supply_view_objects``.

* The ``supply_view_objects`` function determines which widgets are
  enabled for the given page. It then loops over each and calls their
  ``apps.widgets.<widget-name>.views.supply`` function with the
  current ``request`` and ``page_name``.

So go get the player's name, team, and points to the Hello World
widget we need to implement the ``supply`` function. The function
needs to create a dictionary with the keys ``name``, ``team``, and
``points``. Let's take a look at a start to the ``supply`` function::

  """Provide the view for the Hello_World widget."""


  def supply(request, page_name):
      """Supply view_objects contents, which are the player name, team and points."""
      _ = page_name
      profile = request.user.get_profile()
      name = profile.name
      team = profile.team


We got the user from the request then got their profile.  The profile
has the player's name and team. Now how are we going to get the
player's points?  Makahiki provides a ``score_mgr`` that encapsulates
scores. The function we want is ``players_points``. Let's take a look
at the supply function again::


  """Provide the view for the Hello_World widget."""
  from apps.managers.score_mgr import score_mgr


  def supply(request, page_name):
      """Supply view_objects contents, which are the player name, team and points."""
      _ = page_name
      profile = request.user.get_profile()
      name = profile.name
      team = profile.team
      points = score_mgr.player_points(profile)
      return {
              "name": name,
	      "team": team,
	      "points": points,
	     }

*Notice:* we have to import the score_mgr to be able to use it.
Setting up the dictionary is the last step for our supply function.


Add your widget to the installed widget apps
--------------------------------------------
In order for a new widget to be available to the system, you need to
edit the makahiki/settings.py file and add your widget name to the
INSTALLED_WIDGET_APPS variable.  Here is what this portion of the
settings.py file looks like after I've added the new hello_world
widget to it::

  ################################
  # INSTALLED Widgets
  ################################
  INSTALLED_WIDGET_APPS = (
    'action_feedback',
    'ask_admin',
    'badge_scoreboard',
    'badges',
    'bonus_points',
    'hello_world',
    'home',
    'resource_goal',
    'resource_goal.energy',
    'resource_goal.water',
    'energy_power_meter',
    'resource_scoreboard',
    'resource_scoreboard.energy',
    'resource_scoreboard.water',
    'my_achievements',
    'my_commitments',
    'my_info',
    'popular_tasks',
    'prizes',
    'quests',
    'raffle',
    'scoreboard',
    'participation',
    'smartgrid',
    'team_members',
    'upcoming_events',
    'wallpost',
    'help.intro',
    'help.faq',
    'help.rule',
    'status',
    'status.prizes',
    'status.rsvps',
    'status.users',
    'status.actions',
    'logging',
    'status.referrals',
    'status.wattdepot',
    'status.twitter',
    'status.badges',
    'status.DEGG',
    'status.DWGG',
    'wallpost.user_wallpost',
    'wallpost.system_wallpost',
  )

In other words, add the name of your new widget to this list.

Add the widget to a page
------------------------

There are two steps to adding a new widget to an existing page.

1. Edit the Html for the page to include the widget.

   For this tutorial we'll be adding the Hello World widget to the
   profile page. Let's add the widget to the left-hand column. Here's
   the body of the profile page::

      {% block body %}
      <div class="container-fluid">
        <div class="row-fluid">
            <!-- left column -->
            <div class="span6">
                {% if view_objects.my_info %}
                    {% include "widgets/my_info/templates/index.html" %}
                {% endif %}
            </div>

            <!-- right column -->
            <div class="span6">
                {% if view_objects.badges != None %}
                <div class="content-box">
                    {% include "widgets/badges/templates/index.html" %}
                </div>
                {% endif %}
                {% if view_objects.my_commitments %}
                    {% include "widgets/my_commitments/templates/index.html" %}
                {% endif %}
                {% if view_objects.my_achievements %}
                <div class="content-box">
                    {% include "widgets/my_achievements/templates/index.html" %}
                </div>
                {% endif %}
            </div>
        </div>
      </div>
      {% endblock %}

   Currently, the left-hand column only has one widget in it,
   ``my_info``. The right-hand column has three widgets, ``badges``,
   ``my_commitments``, and ``my_achievements``. To add the hello_world
   widget we just have to follow the template and add::

                {% if view_objects.hello_world %}
                    {% include "widgets/hello_world/templates/index.html" %}
                {% endif %}
     
   After the ``my_info`` widget.  The HTML of the page shows all the
   possible widgets displayed on the page. Not all of them may appear.
   
   If we run the server and take a look at the profile page we can see
   that the Hello World widget doesn't appear.

   .. figure:: figs/hello-world-dev/profile-before.png
      :width: 600 px
      :align: center

   We need to complete the next step to enable the widget.

2. Add the widget to the page in the admin interface.  Go to the Admin
   interface, "Settings" page, and select ``Page infos``. It is the
   tenth item in the ``Internal Admin`` section.

   .. figure:: figs/hello-world-dev/page-infos.png
      :width: 600 px
      :align: center

   Select the ``profile`` row in the ``Page Info`` page. The ``Page
   Settings`` section lists the Games and Widgets for the selected
   page.

   .. figure:: figs/hello-world-dev/page-settings.png
      :width: 600px
      :align: center

   Add the ``hello-world`` widget by pressing *Add another Page
   Setting*. Then use the *widget* dropdown and select the
   ``hello-world`` widget. Save the ``profile`` page setting.

   .. figure:: figs/hello-world-dev/pageinfo-w-hello.png
      :width: 600px
      :align: center

   Once the widget is added to the Page Settings the Game Designer may
   enable or disable the widget.



Verify your widget installation
------------------------------

Go to the Profile page, and see the Hello World widget.
 
The following figure shows a portion of the Profile page after choosing the brand new google theme:

.. figure:: figs/hello-world-dev/hello-world-widget.png
   :width: 600 px
   :align: center

   *The newly installed and enabled Hello World Widget.*


Push your changes
-----------------

The final step is to use git to add your new widget and push your changes to your GitHub repository.










