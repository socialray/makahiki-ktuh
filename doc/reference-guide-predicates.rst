.. _section-predicates:

Supported Predicates
====================

This section documents the predicates available for evaluating
conditions such as unlocking smartgrid levels, actions, quests, badges etc.

.. note::  This documentation is extracted automatically from the predicate definition source
           files.  For this reason, the documentation shows the full path to the predicates.
           To use the predicates in a condition string, only the predicate name (without any
           qualified prefixes) should be used. In addition, the "user" argument need not to be
           supplied in the condition string. The predicates can be connected using python boolean
           operators such as "and" or "or" etc.

Example:
The following condition string will check for if the current time has reach round 2
and the user has earned 100 points:
::

    reached_round("Round 2") or has_points(100)

Challenge Predicates
--------------------

.. automodule:: apps.managers.challenge_mgr.predicates
   :members:

Player Predicates
-----------------

.. automodule:: apps.managers.player_mgr.predicates
   :members:

Smart Grid Game Predicates
--------------------------

.. automodule:: apps.widgets.smartgrid.predicates
   :members:





