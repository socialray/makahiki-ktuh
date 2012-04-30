"""Canopy test."""

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from apps.managers.challenge_mgr import challenge_mgr


class CanopyFunctionalTestCase(TestCase):
    """Canopy test case."""

    def setUp(self):
        """setup."""
        self.user = User.objects.create_user("user", "user@test.com", password="atest")
        profile = self.user.get_profile()
        profile.name = "Test U."
        profile.setup_complete = True
        profile.setup_profile = True
        profile.save()

        challenge_mgr.register_page_widget("advanced", "canopy_member")

        self.client.login(username="user", password="atest")

    def testUserAccess(self):
        """Check that superusers, staff, and canopy members can access the canopy."""
        # Test that regular user cannot access the canopy.

        #response = self.client.get(reverse("advanced_index"))
        #self.failUnlessEqual(response.status_code, 404)

        # Test that a superuser can access the canopy
        self.user.is_superuser = True
        self.user.save()
        response = self.client.get(reverse("advanced_index"))
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'alt="Photo of Test U."', count=1)

        # Test that staff can access the canopy
        self.user.is_superuser = False
        self.user.is_staff = True
        self.user.save()
        response = self.client.get(reverse("advanced_index"))
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'alt="Photo of Test U."', count=1)

        # Test that canopy members can access the canopy
        self.user.is_staff = False
        self.user.save()
        profile = self.user.get_profile()
        profile.save()
        response = self.client.get(reverse("advanced_index"))
        self.failUnlessEqual(response.status_code, 200)

    def testDirectory(self):
        """test canopy member directory."""
        profile = self.user.get_profile()
        profile.canopy_member = True
        profile.save()

        response = self.client.get(reverse('canopy_members'))
        self.failUnlessEqual(response.status_code, 200)
