"""Celery Task definitions for smartgrid game."""

from celery.task import task
from apps.widgets.participation import participation
from apps.widgets.smartgrid import smartgrid


@task
def send_reminders():
    """send reminders."""
    smartgrid.send_reminders()
    smartgrid.check_new_submissions()
    participation.award_participation()


@task
def process_notices():
    """Send out notifications such as round transition, commitment end,
    and process rsvp reminder and penalty."""
    smartgrid.notify_round_started()
    smartgrid.notify_commitment_end()
    smartgrid.process_rsvp()
    smartgrid.check_daily_submissions()
