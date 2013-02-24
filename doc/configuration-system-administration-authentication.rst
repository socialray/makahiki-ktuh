.. _section-configuration-system-administration-authentication:


Configure authentication
========================

About authentication
--------------------

In Makahiki, "authentication" refers to the way in which a player logs in to participate
in a challenge.  In Makahiki, there is currently no way for people to "register"
themselves and obtain an account to play a challenge.  Instead, the administrator must
configure the system in advance of the challenge with the names of all potential players,
and the teams to which they are assigned.  (This constraint could be removed in a future
release.)

Given that the system knows in advance the identities of all potential players of a
challenge, the next question is how to verify that a given online user is one of these
potential players?  That is the goal of authentication, and Makahiki provides a variety of
ways to do it. 

.. note:: Authentication is **required** in Makahiki.  If you want the simplest
   authentication to configure, do internal authentication. However, that means your users
   will have a separate account and password for the challenge, which is a barrier to participation.


Getting to the authentication page
----------------------------------

From the Settings Page, click on the System Administration button to retrieve the following
authentication configuration form:

.. figure:: figs/configuration/configuration-system-administration-authentication.png
   :width: 600 px
   :align: center

Makahiki currently supports three kinds of authentication: CAS, LDAP, and the
internal authentication provided by Django.   System administrators must configure at
least one form of authentication, though multiple forms are also acceptable.

CAS authentication
------------------

.. todo:: Document CAS authentication configuration procedure


LDAP authentication
-------------------

.. todo:: Document LDAP authentication configuration procedure


Internal authentication
-----------------------

.. todo:: Document internal authentication configuration procedure
























