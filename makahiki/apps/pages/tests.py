"""
Tests for the pages module.
"""
from django.contrib.auth.models import User

from apps.test_helpers.selenium_helpers import MakahikiSeleniumTestCase
from apps.test_helpers.test_utils import TestUtils

class LandingSeleniumTestCase(MakahikiSeleniumTestCase):
    """
    Selenium tests for the home page.
    """
    fixtures = ["base_teams.json", "base_pages.json"]
        
    def testLanding(self):
        """Test getting the landing page."""
        self.selenium.get('%s%s' % (self.live_server_url, "/"))
        self.selenium.find_element_by_id("landing-button-participant")
        
    def testLogin(self):
        """Test logging in the user to the system."""
        username = "atestuser"
        password = "atestpass"
        TestUtils.setup_user(username, password)
        
        self.login(username, password)
        self.logout()
        
