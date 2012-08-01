"""
Tests for the pages module.
"""
from apps.utils import test_utils
from apps.utils.selenium_helpers import MakahikiSeleniumTestCase
from apps.managers.challenge_mgr import challenge_mgr


class LandingSeleniumTestCase(MakahikiSeleniumTestCase):
    """Selenium tests for the home page."""

    def testLanding(self):
        """Test getting the landing page."""
        self.selenium.get('%s%s' % (self.live_server_url, "/landing/"))
        self.selenium.find_element_by_id("landing-button-participant")

    def testLogin(self):
        """Test logging in the user to the system."""
        username = "atestuser"
        password = "atestpass"
        test_utils.setup_user(username, password)
        challenge_mgr.register_page_widget("home", "home")
        self.login(username, password)
        self.selenium.get('%s%s' % (self.live_server_url, "/home/"))
        try:
            self.assertEqual("Kukui Cup: Home", self.selenium.title)
        except AssertionError, e:
            print e
        self.logout()

    def testPages(self):
        """Test accessing all the pages in the system."""
        username = "atestuser"
        password = "atestpass"
        test_utils.setup_user(username, password)

        challenge_mgr.register_page_widget("home", "home")
        challenge_mgr.register_page_widget("learn", "home")
        challenge_mgr.register_page_widget("energy", "home")
        challenge_mgr.register_page_widget("water", "home")
        challenge_mgr.register_page_widget("news", "home")
        challenge_mgr.register_page_widget("profile", "home")
        challenge_mgr.register_page_widget("help", "home")
        challenge_mgr.register_page_widget("win", "win")
        challenge_mgr.register_page_widget("status", "status")
        challenge_mgr.register_page_widget("about", "about")

        self.login(username, password)

        try:
            self.selenium.get('%s%s' % (self.live_server_url, "/home/"))
            self.assertEqual("Kukui Cup: Home", self.selenium.title)
            self.selenium.get('%s%s' % (self.live_server_url, "/learn/"))
            self.assertEqual("Kukui Cup: Learn", self.selenium.title)
            self.selenium.get('%s%s' % (self.live_server_url, "/energy/"))
            self.assertEqual("Kukui Cup: Energy", self.selenium.title)
            self.selenium.get('%s%s' % (self.live_server_url, "/water/"))
            self.assertEqual("Kukui Cup: Water", self.selenium.title)
            self.selenium.get('%s%s' % (self.live_server_url, "/news/"))
            self.assertEqual("Kukui Cup: News", self.selenium.title)
            self.selenium.get('%s%s' % (self.live_server_url, "/win/"))
            self.assertEqual("Kukui Cup: Win", self.selenium.title)
            self.selenium.get('%s%s' % (self.live_server_url, "/profile/"))
            self.assertEqual("Kukui Cup: Profile", self.selenium.title)
            self.selenium.get('%s%s' % (self.live_server_url, "/help/"))
            self.assertEqual("Kukui Cup: Help", self.selenium.title)
            self.selenium.get('%s%s' % (self.live_server_url, "/status/"))
            self.assertEqual("Kukui Cup: Status", self.selenium.title)
            self.selenium.get('%s%s' % (self.live_server_url, "/about/"))
            self.assertEqual("Kukui Cup: Welcome to KukuiCup!", self.selenium.title)
        except AssertionError, e:
            print e
