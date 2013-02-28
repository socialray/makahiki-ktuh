Enhancement Ideas
=================

This chapter describes some enhancement projects for Makahiki that we believe would be
interesting and useful for the framework. 

Real-time player awareness
--------------------------

It is not possible in Makahiki to know who is currently "on line" and playing the game.
Creating this awareness opens up new social gaming opportunities (performing tasks together), new
opportunities for communication (chat windows), and potentially entirely new games (play
"against" another online player).  

The goal of this enhancement is to extend the framework with a general purpose API that
provides the identities of those who are online, and then the development of one or more
user interface enhancements to exploit this capability. 

Deep Facebook integration
-------------------------

Makahiki currently supports a "shallow" form of Facebook integration: you can request that
your Facebook photo be used as your Makahiki profile picture, and you are given an
oppportunity to post to Facebook when the system notifies you of an accomplishment.

For this task, expand the current Facebook integration. One way is to deepen the
connection between user Facebook pages and their game play.  This might involve more automated
forms of notification (i.e. the same way Spotify playlists are posted to your Facebook
wall), or ways in which your activities on Facebook could impact on your Makahiki
challenge status (for example, posting a sustainability video to Facebook, or liking a
Sustainability organization could earn you points.)  

A different type of enhancement is to allow challenge designers to specify a Facebook page
as the official Challenge Facebook information portal, and have the system automatically
post information to that Facebook page as the challenge progresses.

Action Library Management System
--------------------------------

Makahiki currently ships with over 100 possible "actions" already developed for the Smart
Grid Game.  However, the current implementation suffers from a number of problems:

  * *There is no convenient way to display and peruse the current set of actions.* This
    has led to a duplicate representation of the smart grid game, implemented using a
    `Google Docs spreadsheet linked to Google Sites pages`_. This approach has a lot of
    problems: it duplicates content, it does not provide a way to edit or manage content,
    it is already out of date. 

  * *The content is intimately tied to the Smart Grid Game implementation.*  The SGG is
    just one of many ways that the sustainability content could be presented to players.
    By separating "content" from the "presentation", more games can be developed using
    this content. 

.. _Google Docs spreadsheet linked to Google Sites pages: https://docs.google.com/spreadsheet/ccc?key=0An9ynmXUoikYdE4yaWRPVTlZdTg2Y1V5SWNTeUFjcWc#gid=2

For this task, you will enhance Makahiki to provide a "content management system" for
"actions".  This involves the following changes to the current system:

  * A new set of database tables must be defined to hold Library actions. 
  * Library actions can be "instantiated" (i.e. copied) into the Smart Grid Game. At that
    point they are assigned a category and a row within the Smart Grid Game. 
  * An editor is provided to create action content and preview it in a formatted manner. 
  * A new set of pages can be (optionally) made available to allow others to peruse
    Library content.  
  * Library content can be exported and imported into systems in order to support
    sharing.  A public repository can be provided on GitHub.  The format is likely JSON.
