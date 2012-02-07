Management Commands
===================


Mahahiki implements the following `Django management commands`_ to facilitate setup and management of challenges. 

**Note: This documentation is based on Makahiki 1 and location/availability of these commands may have changed.**

.. _Django management commands: https://docs.djangoproject.com/en/1.3/howto/custom-management-commands

regenerate_codes (slug1 slug2 …)
--------------------------------

Regenerate the confirmation codes for activities that use confirmation
codes. The amount of codes generated is based on the activity’s
``event_max_seat`` attribute. By default, this command will regenerate
codes for all activities with confirmation codes. The command also takes
optional parameters to delete the codes for an activity with the
specified slug(s).

*Implemented in apps/components/activities/management/regenerate_codes.py*


add_codes num_codes slug1 (slug2 …)
-------------------------------------

Add num_codes to activities with the specified slug(s).

*Implemented in apps/components/activities/management/add_codes.py*


send_reminders
---------------

Sends any unsent reminders at the time this script is written. Meant to
be run every hour to send email/text reminders.

*Implemented in apps/components/activities/management/send_reminders.py*


add_points username points short-message long-message
------------------------------------------------------

Give the user additional points. short-message is stored in the
PointTransaction log and displayed in ‘My Achievements’. long-message is
displayed in a user notification.

*Implemented in apps/components/makahiki_base/management/add_points.py*


add_points residence-hall floor-number points short-message long-message
-------------------------------------------------------------------------

Give the members of the residence-hall and floor-number additional
points. short-message is stored in the PointTransaction log and
displayed in ‘My Achievements’. long-message is displayed in a user
notification.

*Implemented in apps/components/makahiki_base/management/add_points.py*

load_users filename
--------------------

Load and create the users from a csv file containing lounge, name, and
email. if the second argument is RA, the csv file is the RA list,
consists of name, email, lounge.

*Implemented in apps/components/makahiki_base/management/load_users.py*
 
reset_competition
------------------

Restores the competition to a pristine state. This means that all wall
posts, activity/commitment/quest members, email/text reminders, raffle
tickets, energy goals, and badge awards are deleted. Points for every
user for every round are also set to 0.

*Implemented in apps/components/makahiki_base/management/reset_competition.py*
 
reset_user username1 (username2 …)
-----------------------------------

Takes usernames as arguments and resets each user, preserving their
username, first and last name, email address, display name, admin
status, and floor/lounge.

Example usage::

  python manage.py reset_user user

*Implemented in apps/components/makahiki_base/management/reset_user.py*

sim_competition
----------------

Simulates activity in the competition up to round 2. Has not been run in
a while and may need an update.

*Implemented in apps/components/makahiki_base/management/sim_competition.py*

validate_users
---------------

Validates usernames of users and makes sure they are unique. Also checks
if any users have multiple profiles.

*Implemented in apps/components/makahiki_base/management/validate_users.py*
 
pick_winners
-------------

Picks raffle winners for any raffle prizes whose raffle deadline has
passed and has not yet been assigned a winner.

*Implemented in apps/components/prizes/management/pick_winners.py*
 
verify_quests
--------------

This command goes through the existing quests and applies their unlock
and completion condition strings to a random user. The command will
report the condition strings that do not validate.

Example usage::

  python manage.py verify_quests

*Implemented in apps/components/quests/management/verify_quests.py*




