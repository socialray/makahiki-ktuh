"""
Tests for the pages module.
"""
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class LandingSeleniumTests(LiveServerTestCase):
    """
    Selenium tests for the home page.
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up for all tests in this class.
        """
        cls.selenium = WebDriver()
        super(LandingSeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        """
        Tear down for all tests in this class.
        """
        super(LandingSeleniumTests, cls).tearDownClass()
        cls.selenium.quit()

    def testLanding(self):
        """
        Test getting the home page and logging in.
        """
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
