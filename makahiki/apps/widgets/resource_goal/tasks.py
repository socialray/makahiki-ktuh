"""Celery Task definitions."""

from celery.task import task
from apps.widgets.resource_goal import resource_goal


@task
def check_energy_goal():
    """update energy usage."""
    resource_goal.check_all_daily_resource_goals("energy")


@task
def check_water_goal():
    """update fake water usage."""
    resource_goal.check_all_daily_resource_goals("water")
