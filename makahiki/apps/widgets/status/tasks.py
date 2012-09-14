"""Celery Task definitions for status."""

from celery.task import task
import datetime
from apps.widgets.status import status


@task
def update_daily_status():
    """update daily status."""
    print '****** Processing daily user count update at %s.*******\n' % datetime.datetime.today()

    status.update_daily_status()
