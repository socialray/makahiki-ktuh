"""
Restore the competition to a pristine state.
"""
import datetime

from django.core import management

from managers.player_mgr.models import Profile, PointsTransaction
from managers.team_mgr.models import Post
from widgets.canopy.models import Post as CanopyPost
from widgets.smartgrid.models import EmailReminder, TextReminder, ActivityMember, CommitmentMember
from widgets.quests.models import QuestMember
from widgets.prizes.models import RaffleTicket
from widgets.energy.models import TeamEnergyGoal
from lib.brabeion.models import BadgeAward

class Command(management.base.BaseCommand):
    """ reset competition command
    """
    help = 'Restore the competition to a pristine state.'

    def handle(self, *args, **options):
        """
        Restores the competition to a pristine state.
        """
        self.stdout.write(
            "WARNING: This command will reset the competition to a pristine state. " +\
            "Points, wall posts, energy goals, raffle tickets, and activity/commitment/quest " +\
            "memberships will be removed.")
        self.stdout.write("\n\nThis process is irreversible.\n")
        value = raw_input("Do you wish to continue  (Y/n)? ")
        while value != "Y" and value != "n":
            self.stdout.write("Invalid option  %s\n" % value)
            value = raw_input("Do you wish to continue  (Y/n)? ")
        if value == "n":
            self.stdout.write("Operation  cancelled.\n")
            return

        self._reset_points()
        self._delete_points_log()
        self._delete_reminders()
        self._delete_memberships()
        self._delete_raffle_tickets()
        self._delete_energy_goals()
        self._delete_badges()
        self._delete_posts()

    def _reset_points(self):
        """
        reset points
        """
        self.stdout.write('Resetting points.\n')
        for profile in Profile.objects.all():
            profile.points = 0
            profile.last_awarded_submission = datetime.datetime.today()
            profile.save()

            for entry in profile.scoreboardentry_set.all():
                entry.points = 0
                entry.last_awarded_submission = datetime.datetime.today()
                entry.save()

    def _delete_points_log(self):
        """delete points log"""
        self.stdout.write('Deleting points transactions.\n')
        PointsTransaction.objects.all().delete()

    def _delete_posts(self):
        """delete posts"""
        self.stdout.write('Deleting team posts.\n')
        Post.objects.all().delete()
        self.stdout.write('Deleting canopy posts.\n')
        CanopyPost.objects.all().delete()

    def _delete_reminders(self):
        """delete reminders
        """
        self.stdout.write('Deleting email reminders.\n')
        EmailReminder.objects.all().delete()
        self.stdout.write('Deleting text reminders.\n')
        TextReminder.objects.all().delete()

    def _delete_memberships(self):
        """delete memberships"""
        self.stdout.write('Deleting quest memberships.\n')
        QuestMember.objects.all().delete()
        self.stdout.write('Deleting activity memberships.\n')
        ActivityMember.objects.all().delete()
        self.stdout.write('Deleting commitment memberships.\n')
        CommitmentMember.objects.all().delete()

    def _delete_raffle_tickets(self):
        """delete raffle tockets"""
        self.stdout.write('Deleting raffle tickets.\n')
        RaffleTicket.objects.all().delete()

    def _delete_energy_goals(self):
        """delete energy goals"""
        self.stdout.write('Deleting energy goals.\n')
        TeamEnergyGoal.objects.all().delete()

    def _delete_badges(self):
        """delete badges"""
        self.stdout.write('Deleting badge awarded objects.\n')
        BadgeAward.objects.all().delete()