"""Invocation:  python manage.py verify_smartgrid

Verifies that all of the existing smartgrid unlock condition strings are valid.
Prints out the names of any invalid conditions."""

from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand
from apps.utils import utils

from apps.widgets.smartgrid.models import Action, Level


class Command(MakahikiBaseCommand):
    """command"""
    help = "Verifies that all existing smartgrid unlock conditions are valid."

    def handle(self, *args, **options):
        """handle"""
        print "Validating smartgrid ..."
        for action in Action.objects.all():
            error_msg = utils.validate_predicates(action.unlock_condition)
            if error_msg:
                print "Unlock conditions '%s' for action '%s' did not validate: %s" % (
                    action.unlock_condition, action.name, error_msg)

        for level in Level.objects.all():
            error_msg = utils.validate_predicates(level.unlock_condition)
            if error_msg:
                print "Unlock conditions '%s' for level '%s' did not validate: %s" % (
                    level.unlock_condition, level.name, error_msg)

        print "All smartgrid conditions are valid."
