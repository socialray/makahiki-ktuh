Testing
=======

This document contains notes on writing and executing tests.

Run ``python manage.py test`` to run all of the tests.

You can also run tests for individual apps by passing in those apps as
parameters. For example, ``python manage.py test widgets.profile`` will
run the tests in ``apps/widgets/profile``.

Creating Selenium Tests
-----------------------

There are two ways to create Selenium tests; by hand or using the 
Selenium IDE. If you choose to write them yourself, the Python WebDriver
API (http://readthedocs.org/docs/selenium-python/en/latest/api.html)
has a list of functions that might be useful when creating tests. While
tedious, it will prevent you from running into compatibility errors.

The other way is to use the Selenium IDE plugin for Firefox. Using the 
Selenium IDE, your actions on the website can be recorded and then 
exported to Python. Use Firefox and go to [[http://seleniumhq.org/download/]] 
to download and install the plugin. After it is downloaded, restart Firefox 
to complete the installation.

Next, start up a test server using
``python manage.py testserver fixtures/*``. This creates a test database
(separate from your development database) and loads the fixture data.

In Firefox, go to ``http://localhost:8000``. Start the Selenium IDE by
going to Tools->Selenium IDE. By default, it starts recording once you
open the IDE. Create your test by navigating through the site as a user
would. You have access to additional test assertion commands by right
clicking on the page. However, the downside of the IDE is that not all
of the Selenium assertions work when exported to the WebDriver format 
that Django will use.

Once you are done, click on the red “record” icon on the Selenium IDE to
stop it from recording. You can then export your test by going to
“File->Export Test Case As->Python 2 (WebDriver)”. 

Once the test is exported, it still needs to be edited to fit within our
framework.

Editing exported Selenium tests to run within our test framework
----------------------------------------------------------------

When the test is exported, it needs to be edited a little to support our
test framework. By default, a test comes out something like this.
::

    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select
    from selenium.common.exceptions import NoSuchElementException
    import unittest, time, re

    class Test(unittest.TestCase):
        def setUp(self):
            self.driver = webdriver.Firefox()
            self.driver.implicitly_wait(30)
            self.base_url = "http://localhost:8000/"
            self.verificationErrors = []
    
        def test_(self):
            driver = self.driver
            driver.get(self.base_url + "/account/login/")
    
        def tearDown(self):
            self.driver.quit()
            self.assertEqual([], self.verificationErrors)

    if __name__ == "__main__":
        unittest.main()

Things that need to be changed:

- Delete the existing imports. Instead, import MakahikiSeleniumTestCase from
  apps.test_helpers.selenium_helpers and test_utils from apps.test_helpers.
- Change the Test class to inherit from MakahikiSeleniumTestCase.
- Remove the setUp and tearDown methods. These are handled for you in
  MakahikiSeleniumTestCase. Note that MakahikiSeleniumTestCase has a few useful
  functions, like ``login(username, password)`` and ``logout()``.
- After the class definition, add in a few base test fixtures
  (i.e. `fixtures = ["test_teams.json", "base_pages.json"]`). You may want to
  enter additional fixtures from the fixtures directory. The two fixtures in
  the example are highly recommended unless you have a specific reason not to
  include them.
- Remove the if statement at the end.
- Put in comments and change the name of the test class.
  
After this, your test should look something like this:

::

    """
    Tests for the pages module.
    """
    from apps.test_helpers.selenium_helpers import MakahikiSeleniumTestCase
    from apps.test_helpers import test_utils


    class LandingSeleniumTestCase(MakahikiSeleniumTestCase):
        """Selenium tests for the home page."""
        fixtures = ["test_teams.json", "base_pages.json"]

        def testLogin(self):
            self.login("username", "password")
            self.logout()


