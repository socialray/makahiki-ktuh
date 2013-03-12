.. _section-configuration-game-admin-participation-game:

Design the Participation Game
=============================

About the participation game
----------------------------

One of the current design constraints of the Kukui Cup is that the players associated with
each team in a challenge must be specified in advance of a challenge.  Thus, as the
challenge runs, it is possible to know exactly what percentage of each team's players are
*actively* playing the game (in the sense that they have logged in at least once).

The Participation Game is designed to incentivize active players on a team to recruit
other members of their team to login and try the game.  It does this by providing extra
points to all active players on a team when the percentage participation by that team
reaches certain thresholds (currently 50%, 75%, and 100%).

The current percentage participation by a player's team is shown in a scoreboard when this
game is enabled (as shown in the figure below) and players receive an in-game notification whenever they reach a threshold 
participation where points are awarded.

.. figure:: figs/configuration/challenge-design-game-admin-participation-game-scoreboard.png
   :width: 400 px
   :align: center


Configure the Participation Game
--------------------------------

To configure the participation game, click on the "Participation Settings" link in the
Game Admin widget. 
You will see the overview of the participation settings. Clicking on the link will bring you to a page to change the settings:

.. figure:: figs/configuration/configuration-game-admin-participation-game.png
   :width: 600 px
   :align: center

You can change the points to award for each participation percentage. Currently, the
percentages (50, 75, and 100%) are hardwired into the system.

.. note:: Remember to click the Save button at the bottom of the page when finished to save your changes.

