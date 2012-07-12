"""Celery Task definitions for smartgrid game."""

from celery.task import task
from apps.widgets.smartgrid import smartgrid


@task
def send_reminders():
    """send reminders."""
    smartgrid.send_reminders()


@task
def notify_round_started():
    """notify round transition."""
    smartgrid.notify_round_started()


@task
def notify_commitment_end():
    """notify commitment end."""
    smartgrid.notify_commitment_end()


@task
def process_rsvp():
    """process rsvp reminder and penalty."""
    smartgrid.process_rsvp()
