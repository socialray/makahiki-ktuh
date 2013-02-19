.. _section-configuration-challenge-admin-scheduler-settings:

Configure the Periodic Tasks
============================

After clicking on the "Periodic task Settings" link in the Challenge Design page, a page similar to the following should appear:

.. figure:: figs/configuration/configuration-challenge-admin-scheduler-settings.1.png
   :width: 600 px
   :align: center

This table lists all the defined Periodic Tasks, such as checking the Energy Goals. You may enable, disable, and create new periodic tasks.

Configure a periodic task
-------------------------

.. figure:: figs/configuration/configuration-challenge-admin-scheduler-settings.2.png
   :width: 600 px
   :align: center

Clicking on a task name takes you to a page containing a form that allows you to edit the task attributes or delete the task entirely. The important fields are
Name - The name of the task you see in the list. Task name - This is the function that is run. In this example 'apps.widgets.resource_goal.tasks.check_energy'. 
The "Interval" or "Crontab" fields determine when Makahiki runs the task. In this case it is run every day at 23:55. If the task needs parameters supply them
in the Arguments field. Check or uncheck the Enabled field to turn the task on or off. 


.. note:: Remember to click the Save button at the bottom of the page when finished to save your changes. 

