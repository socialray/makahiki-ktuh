"""Celery Task definitions for smart grid game."""

from celery.task import task
import datetime
from apps.managers.challenge_mgr import challenge_mgr
from apps.widgets.badges import badges
from apps.widgets.participation import participation
from apps.widgets.smartgrid import smartgrid


@task
def send_reminders():
    """send reminders."""
    print '****** Processing send_reminders at %s *******' % datetime.datetime.today()

    challenge_mgr.init()
    smartgrid.send_reminders()
    smartgrid.check_new_submissions()
    participation.award_participation()


@task
def process_notices():
    """Send out notifications such as commitment end,
    and process rsvp reminder and penalty."""
    print '****** Processing notices at %s *******' % datetime.datetime.today()

    challenge_mgr.init()
    smartgrid.notify_commitment_end()
    smartgrid.process_rsvp()
    smartgrid.check_daily_submissions()
    badges.award_possible_daily_badges()


@task
def process_rounds():
    """Send out notifications such as round transition."""
    print '****** Processing rounds at %s *******' % datetime.datetime.today()

    challenge_mgr.init()
    smartgrid.notify_round_started()
