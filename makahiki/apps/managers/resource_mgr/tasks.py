"""Celery Task definitions."""

from celery.task import task
from apps.managers.resource_mgr import resource_mgr


@task
def update_energy_usage():
    """update energy usage."""
    resource_mgr.update_energy_usage()


@task
def update_fake_water_usage():
    """update fake water usage."""
    resource_mgr.update_fake_water_usage()
