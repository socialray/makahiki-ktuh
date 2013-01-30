.. _section-configuration-settings:

Retrieve Settings Page
======================

Log in as admin
---------------

To login as an administrator, go to the internal (Django) login page at: http://127.0.0.1:8000/account/login:

.. figure:: figs/configuration/configuration-account-login.png
   :width: 600 px
   :align: center

Use the credentials you specified in the MAKAHIKI_ADMIN_INFO environment variable. 

Upon successful login, you will be taken to the home page:

.. figure:: figs/configuration/configuration-admin-home.png
   :width: 600 px
   :align: center

Note that admin accounts have two additional pages displayed in the Nav Bar:  "Status" and
"Settings".  "Status" provides real time analytics for use in managing a running
competition, as detailed in :ref:`section-execution`.

Click on Settings page icon
---------------------------

Click on the Settings icon in the Nav Bar to go to the Settings page:

.. figure:: figs/configuration/configuration-settings.png
   :width: 600 px
   :align: center

This page presents a set of Django-styled widgets (Challenge, Player, Resource, etc.) that
provide access to pages that allow configuration of all of the various aspects of
a Makahiki challenge.

The following sections document these configuration widgets.

