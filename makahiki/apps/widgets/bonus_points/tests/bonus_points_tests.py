'''
Created on Aug 4, 2012

@author: cmoore
'''
from apps.utils import test_utils
from apps.managers.challenge_mgr import challenge_mgr
from django.test.testcases import TransactionTestCase
from apps.widgets.bonus_points.models import BonusPoint
from django.core.urlresolvers import reverse


class BonusPointTest(TransactionTestCase):
    """Bonus Points Test."""

    def setUp(self):
        """setup"""
        self.user = self.user = test_utils.setup_user(username="user", password="changeme")

        challenge_mgr.register_page_widget("learn", "smartgrid")

        self.client.login(username="user", password="changeme")

    def testViewBonusPoint(self):
        """Test view bonus points."""
        BonusPoint.generate_bonus_points(5, 5)
        BonusPoint.generate_bonus_points(10, 2)
        BonusPoint.generate_bonus_points(20, 3)

        response = self.client.get(reverse('bonus_view_codes'))
        self.failUnlessEqual(response.status_code, 404)

        self.user.is_staff = True
        self.user.save()

        response = self.client.get(reverse('bonus_view_codes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_bonus_points.html')
