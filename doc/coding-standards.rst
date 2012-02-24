Coding Standards
================

This document contains information to support uniform, high quality, and
efficient development of Makahiki.

Pylint
------

All code should pass `Pylint`_.   To run pylint::

  % cd makahiki/
  % scripts/run_pylint.sh

.. _Pylint: http://pypi.python.org/pypi/pylint

General documentation string standards
--------------------------------------

Documentation strings should be enclosed in triple double quotes.  

Documentation strings should be formatted using `reStructuredText`_ format
so that they can be easily processed using the Sphinx `autodoc`_ extension.

.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _autodoc: http://sphinx.pocoo.org/ext/autodoc.html


The first line of a documentation string (i.e. the line containing the open
triple double quote) should contain a one sentence summary of the purpose
of the program unit (module, class, function, variable, etc.)

If one sentence suffices to document the program unit, then the closing triple
double quote should appear on the same line. 

Otherwise there should be a blank line followed by additional lines of
documentation.  In this case, the closing triple double quote appears on
its own line.

Module documentation
--------------------

Every module (i.e. .py file) should have a documentation string explaining
its purpose and (if relevant) client interface.   

The module documentation string should not specify the file name. 

For example, here is an example docstring for the `apps/pages/views.py`_
module::

  """Provides the top-level rendering functions for all makahiki pages.

  This module handles all requests for Makahiki pages.  It handles
  authentication and contains the code to dynamically render the custom
  configured pages for any particular site.
  """

Function documentation
----------------------

All functions should have a documentation string explaining its purpose and 
documenting parameters and any return values.    

See the `Info field lists`_ page for helpful information on how to format
parameter lists and return values appropriately.

.. _Info field lists: http://sphinx.pocoo.org/domains.html#info-field-lists

For example, here is an example docstring for the index(request) method
appearing in the `apps/pages/views.py`_ module::

  """Process the request, dynamically generating the page as specified in page_settings.

  :param request The django request object. 
  :return The response object for the page.
  """

.. _apps/pages/views.py: https://github.com/csdl/makahiki/blob/master/makahiki/apps/pages/views.py

Variable documentation
----------------------

All variables should have a documentation string explaining its purpose and
who might reference it. 

Variables should be documented by a documentation string immediately
following the variable declaration. For example::

  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': 'dev.db',
          'USER': '',
          'PASSWORD': '',
          }
  }
  """Specifies the default database, required by Django."""





  
 



