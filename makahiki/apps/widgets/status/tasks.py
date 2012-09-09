"""Celery Task definitions for status."""

from celery.task import task
from apps.widgets.status import status


@task
def update_daily_status():
    """update daily status."""
    status.update_daily_status()
