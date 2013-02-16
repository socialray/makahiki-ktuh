Coding Standards
================

This document contains information to support uniform, high quality, and
efficient development of Makahiki.

Automated quality assurance
---------------------------

All code should pass `Pylint`_, `PEP 8`_, and the current set of Makahiki unit
tests.   To run them individually::

  % cd makahiki/
  % scripts/run_pylint.sh
  % scripts/run_pep8.sh
  % python manage.py test

.. _Pylint: http://pypi.python.org/pypi/pylint
.. _PEP 8: https://github.com/jcrocholl/pep8

To simplify quality assurance, there is a script called verify.py that runs all of these
scripts::

  % cd makahiki/
  % scripts/verify.py

If all return successfully, then verify.py returns normally and no output is printed.  If there
are any errors, the output associated with the unsuccessful tools is printed
and verify.py returns with an error code. 

It is good practice to run verify.py prior to pushing your code to the
master branch at github. 

Be patient: verify takes 10 seconds or more to complete.

Coverage
--------

To obtain a coverage report on the test cases::

  % scripts/coverage.py

The report will be generated into the directory htmlcov/.  Open index.html
to browse.  Click the coverage column to sort, and click on a module to see
which lines were tested and which lines were not.

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

  :param request: The django request object. 
  :return: The response object for the page.
  """

Note the following:
  * There must be a blank line between the text description and the start
    of the parameter/return value descriptions.
  * The directives must start and end with a ":".  Note that this means the
    param directive includes a trailing ":" after the param name, and the
    return directive has a ":" on both sides. 

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





  
 



