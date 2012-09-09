"""Define the model for DailyStatus."""
from django.db import models


class DailyStatus(models.Model):
    """Stores the number of visitors per day."""

    daily_visitors = models.IntegerField(
        blank=True, null=True,
        help_text="Number of visitors.")
    setup_users = models.IntegerField(
        default=0,
        help_text="Number of users setup their profiles.")
    date = models.CharField('name', unique=True, max_length=50,
        help_text="The date of the status.")
    short_date = models.DateField(
        null=True,
        help_text="The date of the status.")
    updated_at = models.DateTimeField(
        null=True,
        editable=False,
        auto_now=True)

    class Meta:
        """Meta"""
        verbose_name_plural = "Daily status"
