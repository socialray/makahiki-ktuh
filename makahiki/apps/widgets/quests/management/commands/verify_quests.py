"""Invocation:  python manage.py verify_quests

Verifies that all of the existing quest lock and unlock condition strings are valid.
Prints out the names of any invalid quest conditions."""

from apps.managers.challenge_mgr.challenge_mgr import MakahikiBaseCommand
from apps.utils import utils

from apps.widgets.quests.models import Quest


class Command(MakahikiBaseCommand):
    """command"""
    help = "Verifies that all existing quest unlock/completion conditions are valid."

    def handle(self, *args, **options):
        """handle"""
        print "Validating quests ..."
        for quest in Quest.objects.all():
            error_msg = utils.validate_predicates(quest.unlock_conditions)
            if error_msg:
                print "Unlock conditions for '%s' did not validate: %s" % (quest.name, error_msg)

            error_msg = utils.validate_predicates(quest.completion_conditions)
            if error_msg:
                print "Completion conditions '%s' for '%s' did not validate: %s" % (
                    quest.completion_conditions, quest.name, error_msg)

        print "All quests conditions are valid."
