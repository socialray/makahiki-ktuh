Testing
=======

This document contains notes on writing and executing tests.

Creating Selenium Tests Using Selenium IDE
------------------------------------------

To create a Selenium test, we highly recommend using the Selenium IDE
plugin for Firefox. Using the Selenium IDE, your actions on the website
can be recorded and then exported to Python. Use Firefox and go to
[[http://seleniumhq.org/download/]] to download and install the plugin.
After it is downloaded, restart Firefox to complete the installation.

Next, start up a test server using
``python manage.py testserver fixtures/*``. This creates a test database
(separate from your development database) and loads the fixture data.

In Firefox, go to ``http://localhost:8000``. Start the Selenium IDE by
going to Tools->Selenium IDE. By default, it starts recording once you
open the IDE. Create your test by navigating through the site as a user
would. You have access to additional test assertion commands by right
clicking on the page.

Once you are done, click on the red “record” icon on the Selenium IDE to
stop it from recording. You can then export your test by going to
“File->Export Test Case As->Python 2 (Remote Control)”. We recommend
saving these tests in a Selenium subdirectory of the page you are
testing. We also recommend saving a copy of the test case (File->Save
Test Case As) with a .sel extension in the same directory so that we can
open it in the IDE.

Once the test is exported, it still needs to be edited to fit within our
framework.

Editing Selenium tests to run within our test framework
-------------------------------------------------------

When the test is exported, it needs to be edited a little to support our
test framework. By default, a test comes out something like this (with
some comments about the things we’ll edit):

::

    from selenium import selenium # We'll import a Mixin for selenium.
    import unittest, time, re # We don't need to import unittest.  Instead, we will import Django's TestCase.

    class sample_test(unittest.TestCase): # This will inherit from Django's TestCase and the Selenium mixin
        # Optional fixtures can be specified here
        def setUp(self):
            self.verificationErrors = []
            self.selenium = selenium("localhost", 4444, "*chrome", "http://localhost:8000/") # not needed
            self.selenium.start() # not needed

        def test_sample_test(self):
            sel = self.selenium
            sel.open("/")
            try: self.failUnless(sel.is_text_present("Welcome"))
            except AssertionError, e: self.verificationErrors.append(str(e))

        def tearDown(self):
            self.selenium.stop() # Not needed
            self.assertEqual([], self.verificationErrors)

    if __name__ == "__main__":
        unittest.main() 

Things that need to be changed:

-  Replace ``from selenium import selenium`` with
   ``from noseselenium.cases import SeleniumTestCaseMixin``. This
   contains the selenium class as well as some additional useful
   features like loading fixtures.
-  unittest does not need to be imported. Instead, add the import
   statement ``from django.test import TestCase``.
-  Change the class definition to inherit from TestCase (Django’s test
   case) and SeleniumTestCaseMixin. It should read something like
   ``class sample_test(TestCase, SeleniumTestCaseMixin):``.
-  You can import fixtures from the database. For example, to load the
   floors and users fixtures, add the line
   ``selenium_fixtures = ["fixtures/base_floors.json", "fixtures/test_users.json"]``.
-  In setUp, remove the selenium initialization and
   ``self.selenium.start()``. This will be handled by the mixin.
-  In tearDown, remove ``self.selenium.stop()``.

After this, your tests should look something like this:

::

    from noseselenium.cases import SeleniumTestCaseMixin
    import time, re
    from django.test import TestCase

    class sample_test(TestCase, SeleniumTestCaseMixin):
        selenium_fixtures = []

        def setUp(self):
            self.verificationErrors = []

        def test_sample_test(self):
            sel = self.selenium
            sel.open("/")
            try: self.failUnless(sel.is_text_present("Welcome"))
            except AssertionError, e: self.verificationErrors.append(str(e))

        def tearDown(self):
            self.assertEqual([], self.verificationErrors)

    if __name__ == "__main__":
        unittest.main()

Running Selenium tests with the rest of the test suite
------------------------------------------------------

There are a few things you’ll need to do before you run the exported
Python Selenium tests from the command line.

-  Make sure your requirements are up to date. Type
   ``pip install -r requirements.pip`` to install the latest
   requirements.
-  It is HIGHLY recommended that you use a database backend other than
   SQLite3 because of issues with concurrency. To set up a different
   backend, consult Django’s documentation
   [[http://docs.djangoproject.com/en/1.2/topics/install/#get-your-database-running]].
-  Next, you’ll need to have the Selenium server running on your system.
   Download it from the Selenium downloads page
   [[http://seleniumhq.org/download/]]. Once downloaded, it can be
   started using ``java -jar selenium-server.jar``.

After that, you can run the tests by using a Python script that adds the
required parameters. Run ``python runtests.py`` to run all of the tests.
You can also run tests for individual apps by passing in those apps as
parameters. For example, ``python runtests.py pages.view_profile`` will
run the tests in ``apps/pages/view_profile``, including Selenium tests.
