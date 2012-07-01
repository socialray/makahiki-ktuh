"""
Tests for the pages module.
"""
from apps.utils import test_utils
from apps.utils.selenium_helpers import MakahikiSeleniumTestCase


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

        self.login(username, password)
        self.logout()
