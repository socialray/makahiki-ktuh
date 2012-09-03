"""Celery Task definitions."""

from celery.task import task
import datetime
from apps.widgets.resource_goal import resource_goal


@task
def check_energy_goal():
    """update energy usage."""
    date = datetime.datetime.today()
    resource_goal.check_resource_goals("energy", date)


@task
def check_water_goal():
    """update fake water usage."""
    date = datetime.datetime.today()
    resource_goal.check_resource_goals("water", date)
