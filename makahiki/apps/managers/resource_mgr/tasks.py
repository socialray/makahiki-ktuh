"""Celery Task definitions."""

from celery.task import task
import datetime
from apps.managers.resource_mgr import resource_mgr


@task
def update_energy_usage():
    """update energy usage."""
    date = datetime.datetime.today()
    resource_mgr.update_energy_usage(date)


@task
def update_fake_water_usage():
    """update fake water usage."""
    date = datetime.datetime.today()
    resource_mgr.update_fake_water_usage(date)
