"""Bonus Points model definition."""
import datetime
'''
Created on Aug 5, 2012

@author: Cam Moore
'''

import random
from django.db import models, IntegrityError
from django.contrib.auth.models import User


class BonusPoint(models.Model):
    """Represents universal bonus points."""
    point_value = models.IntegerField(default=5)
    code = models.CharField(max_length=50, unique=True, db_index=True,
                            help_text="The confirmation code.")
    is_active = models.BooleanField(default=True, editable=False,
                                    help_text="Is the bonus points still active?")
    user = models.ForeignKey(User, null=True, blank=True,
                             help_text="The user who claimed the bonus points.")
    claim_date = models.DateTimeField(null=True, blank=True,
                                      help_text="The date the user claimed the points.")
    create_date = models.DateTimeField(default=datetime.datetime.now(),
                                       verbose_name="Date created",
                                       help_text="Date Bonus Point code was created.")
    printed_or_distributed = models.BooleanField(default=False, editable=True,
                                help_text="Has the code been printed or distributed.")
    admin_tool_tip = "Challenge Bonus Points"

    def __unicode__(self):
        return self.code

    @staticmethod
    def generate_bonus_points(point_value, num_codes):
        """Generates a set of random codes for the bonus points with the given
        point value."""
        values = 'abcdefghijkmnpqrstuvwxyz234789'

        # Use the first non-dash component of the slug.
        header = 'BONUS'
        header += "-"
        header += str(point_value)
        header += "-"
        for _ in range(0, num_codes):
            bonus = BonusPoint(point_value=point_value, code=header.lower(),
                               create_date=datetime.datetime.now())
            valid = False
            while not valid:
                for value in random.sample(values, 5):
                    bonus.code += value
                try:
                    # print bonus.code
                    # Throws exception if the code is a duplicate.
                    bonus.save()
                    valid = True
                except IntegrityError:
                    # Try again.
                    bonus.code = header
