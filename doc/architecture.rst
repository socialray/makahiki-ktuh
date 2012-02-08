Architecture
============

External architecture
---------------------

Let's begin by illustrating how Makahiki fits into the broader system context.

.. figure:: figs/system-architecture.png
   :width: 600 px
   :align: center

As the figure above shows, Makahiki interfaces with the outside environment in four different ways. 

First, the left side of Makahiki illustrates the primary user interface: that with the players of the challenge implemented by Makahiki.   

Second, the top side illustrates a specialized user interface provided for administrators of the system.  This interface provides access to real-time game analytics, interfaces to administer the various game components, and access to other admin-only services.  

Third, the right side illustrates that Makahiki must obtain real-world environmental data as the challenge progresses in order to provide feedback to users about the impact of their actions. In some cases, environmental data can be input automatically into the system through a combination of "smart" meters and additional services (such as the `WattDepot`_ system for 
energy data collection, storage, and analysis).  If that is not possible, then manual meters
can be read by administrators on a regular (typically daily) basis and input into Makahiki using and administrator interface. 

Fourth, the bottom side illustrates that Makahiki stores its data in a database repository 
(currently `PostgreSQL`_).  To reduce database access and improve performance, Makahiki provides support for caching (currently `memcached`_).

.. _WattDepot: http://wattdepot.googlecode.com/
.. _PostgreSQL: http://www.postgresql.org/
.. _memcached: http://memcached.org/

Finally, the figure shows that Makahiki has three major internal components: authentication and page display, widgets, and managers.  The next section provides more detail on this internal architecture.

Internal architecture
---------------------

The following figure provides a perspective on Makahiki's architecture in terms of three kinds of "components": Django-related infrastructure, Widgets, and Managers.

.. figure:: figs/system-internal-architecture.png
   :width: 600 px
   :align: center

This categorization is intended to provide the following conceptual understanding.

*Managers* are modules that provide Makahiki capabilities that do not involve a (player) user interface.  They might provide interaction with administrators via the Django admin interface.  Managers can implement game mechanic data structures (such as scores, players, and teams) or more generic web service functions (transactions, authorization, etc.) 

*Widgets* are modules that provide Makahiki capabilities that do include a player user interface. Widgets can be roughly characterized in three ways.  "Info widgets" provide state information about the challenge to players but little in the way of interaction.  "Mechanics widgets" provide game elements such as Quests and Badges.  The third category, "game widgets", or "gamelets", refer to full-fledged interactive games. 

*Django components* are modules that provide the web service "glue" to hold the rest of the system together. 







