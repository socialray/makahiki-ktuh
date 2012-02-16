"""
ask admin tests.
"""

#pylint: disable=C0103

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core import mail

from managers.team_mgr.models import Team


class AskAdminFunctionalTests(TestCase):
    """AskAdmin test cases."""
    fixtures = ["base_teams.json"]

    def setUp(self):
        """setup"""
        self.user = User.objects.create_user("user", "user@test.com", password="bogus")
        team = Team.objects.all()[0]
        profile = self.user.get_profile()
        profile.name = 'test'
        profile.team = team
        profile.setup_complete = True
        profile.setup_profile = True
        profile.save()

        self.client.login(username="user", password="bogus")

    def testAjaxPost(self):
        """
        Test that an AJAX post to ask an admin sends an email.
        """
        response = self.client.post(reverse('ask_admin_feedback'), {
            'url': 'http://localhost:8000/test/',
            'question': 'question',
            }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.failUnlessEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(mail.outbox[0].subject.find(self.user.get_profile().name) > 0)

