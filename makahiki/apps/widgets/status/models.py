"""Define the model for DailyStatus."""
from django.db import models


class DailyStatus(models.Model):
    """Stores the number of visitors per day."""

    daily_visitors = models.IntegerField(
        blank=True, null=True,
        help_text="Number of visitors.")
    date = models.DateTimeField(editable=False, auto_now_add=True)
