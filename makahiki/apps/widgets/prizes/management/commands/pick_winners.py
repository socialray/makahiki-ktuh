"""Pick the raffle prize winners."""
import random
from django.core import management
from apps.managers.settings_mgr import get_current_round_info
from apps.widgets.notifications.models import NoticeTemplate, UserNotification
from apps.widgets.raffle.models import RafflePrize


class Command(management.base.BaseCommand):
    """command"""
    help = 'Picks winners for raffle deadlines that have passed.'

    def handle(self, *args, **options):
        """
        Picks winners for raffle deadlines that have passed.
        """
        round_name = get_current_round_info()["name"]
        self.stdout.write("Picking winners for %s prizes\n" % round_name)
        self.__pick_winners(RafflePrize.objects.filter(round_name=round_name,
                                                       winner__isnull=False))

    def __pick_winners(self, prizes):
        """Pick the winner."""
        for prize in prizes:
            if not prize.winner:
                # Randomly order the tickets and then pick a random ticket.
                while True:
                    tickets = prize.raffleticket_set.order_by("?").all()
                    if tickets.count() == 0:
                        self.stdout.write('No tickets for %s. Skipping.\n' % prize)
                    ticket = random.randint(0, tickets.count() - 1)
                    user = tickets[ticket].user
                    self.stdout.write(str(prize) + ": " + user.username + '\n')
                    value = raw_input('Is this OK? [y/n] ')
                    if value.lower() == 'y':
                        prize.winner = user
                        prize.save()

                        self.stdout.write("Notifying %s\n" % user.username)
                        # Notify winner using the template.
                        try:
                            template = NoticeTemplate.objects.get(notice_type='raffle-winner')
                            message = template.render({'PRIZE': prize})
                            UserNotification.create_info_notification(user, message, True, prize)
                        except NoticeTemplate.DoesNotExist:
                            self.stdout.write(
                                "Could not find the raffle-winner template.  "
                                "User was not notified.\n")

                        break
