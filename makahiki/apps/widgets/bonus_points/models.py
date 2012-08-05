"""Bonus Points model definition."""
'''
Created on Aug 5, 2012

@author: Cam Moore
'''

import random
from django.db import models, IntegrityError


class BonusPoints(models.Model):
    """Represents universal bonus points."""
    point_value = models.IntegerField(default=5)
    code = models.CharField(max_length=50, unique=True, db_index=True,
                            help_text="The confirmation code.")
    is_active = models.BooleanField(default=True, editable=False,
                                    help_text="Is the bonus points still active?")

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
            bonus = BonusPoints(point_value=point_value, code=header.lower())
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
