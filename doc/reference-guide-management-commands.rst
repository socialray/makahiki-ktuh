.. _section-developer-guide-management-commands: 

Management Commands
===================


Mahahiki implements the following `Django management commands`_ to facilitate setup and management of challenges. 

.. _Django management commands: https://docs.djangoproject.com/en/1.3/howto/custom-management-commands

Development management
**********************

These management commands are used by developers for testing enhancements to 
the system and debugging.

clear_cache
-----------

.. automodule:: apps.managers.challenge_mgr.management.commands.clear_cache

clear_log
---------

.. automodule:: apps.managers.challenge_mgr.management.commands.clear_log

clear_session
-------------

.. automodule:: apps.managers.challenge_mgr.management.commands.clear_session

setup_test_data
---------------

.. automodule:: apps.managers.challenge_mgr.management.commands.setup_test_data


Challenge configuration
***********************

These management commands are used to set up a challenge.

load_users
----------

.. automodule:: apps.managers.player_mgr.management.commands.load_users

reset_users
-----------

.. automodule:: apps.managers.player_mgr.management.commands.reset_users

verify_quests
-------------

.. automodule:: apps.widgets.quests.management.commands.verify_quests

verify_smartgrid
----------------

.. automodule:: apps.widgets.smartgrid.management.commands.verify_smartgrid

Challenge management
********************

These management commands are used by administrators to facilitate the running of
a challenge.


award_badge
-----------

.. automodule:: apps.widgets.badges.management.commands.award_badge


update_energy_baseline
----------------------

.. automodule:: apps.widgets.resource_goal.management.commands.update_energy_baseline


Automated management
********************

These management commands are typically invoked automatically during a challenge in order
to manage resource and game data.

update_energy_usage
-------------------

.. automodule:: apps.widgets.resource_goal.management.commands.update_energy_usage

check_energy_goal
-----------------

.. automodule:: apps.widgets.resource_goal.management.commands.check_energy_goal

check_water_goal
----------------

.. automodule:: apps.widgets.resource_goal.management.commands.check_water_goal



