.. _section-configuration-challenge-admin-teams-settings:

Design the teams
================

About teams
-----------

Makahiki defines a three level hierarchy consisting of groups, teams, and players.
  * Groups, which collect together a set of teams. Groups are optional.
  * Teams, which collect together a set of players. Teams are required.
  * Players.

For example, a residence hall challenge might consist of three buildings, each with 10
floors, each floor containing 20 residents.   You could define a single group for each building,
10 teams for each group corresponding to the 10 floors in each building, and 20 players
for each team corresponding to the 20 residents on each floor. Thus, groups correspond to
buildings, teams correspond to floors, and players correspond to residents. 

All players are required to be associated with a Team.  This constraint might be removed in a
future release of the system.

.. note:: Configuration of teams is **required**.  At the very least, you should rename
   the two teams to fit your challenge.  You might also need to define more than two teams.

.. todo:: Way too many teams defined in the default instance.  Cut them down to say, two.

.. todo:: Does dasha load the default or the demo instance? It should load the default so
   I can write this documentation correctly.

.. todo:: I tried to delete a team, and got an uninformative error message.   Do I have to
   delete all players associated with a team before deleting it? If so, the error should
   maybe state that.

Getting to the team settings page
---------------------------------

After clicking on the "Teams Settings" link in the Challenge Design page, a page similar to the following should appear:

.. figure:: figs/configuration/configuration-challenge-admin-teams-settings.1.png
   :width: 600 px
   :align: center

To define a new team, click the "Add team" button in the upper right corner. To edit a
team definition, click the link which brings up a page similar to the following:


.. figure:: figs/configuration/configuration-challenge-admin-teams-settings.2.png
   :width: 600 px
   :align: center

Specifying the group is optional. 

.. note:: Remember to click the Save button at the bottom of the page when finished to save your changes. 

