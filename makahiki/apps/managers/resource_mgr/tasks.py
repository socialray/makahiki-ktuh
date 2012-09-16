"""Celery Task definitions."""

from celery.task import task
import datetime
from apps.managers.resource_mgr import resource_mgr
from apps.widgets.resource_goal import resource_goal


@task
def update_energy_usage():
    """update energy usage."""
    date = datetime.datetime.today()
    print '****** Processing energy usage update at %s *******\n' % date

    resource_goal.update_resource_usage("energy", date)


@task
def update_fake_water_usage():
    """update fake water usage."""
    date = datetime.datetime.today()
    print '****** Processing water usage update at %s *******\n' % date

    resource_mgr.update_fake_water_usage(date)
