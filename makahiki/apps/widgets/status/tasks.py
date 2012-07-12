"""Celery Task definitions for update daily status."""

from celery.task import task
import datetime
from apps.managers.player_mgr.models import Profile
from apps.widgets.status.models import DailyStatus


@task
def update_daily_status():
    """update daily status."""
    today = datetime.datetime.today()
    count = Profile.objects.all().filter(last_visit_date__gte=today,
        last_visit_date__lt=today + datetime.timedelta(days=1)).count()
    state = DailyStatus(date=today, daily_visitors=count)
    state.save()
    print 'daily visit count status updated at %s.' % today
