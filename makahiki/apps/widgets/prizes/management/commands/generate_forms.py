"""Generate the hardcopy forms for winners after a round is completed."""
import os
from django.db.models import Q
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.core import management
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.team_mgr.models import Team
from apps.managers.player_mgr.models import Profile
from apps.widgets.raffle.models import RafflePrize
from apps.widgets.prizes.models import Prize


class Command(management.base.BaseCommand):
    """Pick the raffle game winners."""
    help = 'Picks winners for raffle deadlines that have passed.'

    def handle(self, *args, **options):
        """Generates forms for winners."""
        self.__generate_forms(challenge_mgr.get_current_round_info()["name"])

    def __generate_forms(self, round_name):
        """Generate both raffle and prize forms."""
        round_dir = 'prizes/%s' % round_name
        if not os.path.exists('prizes'):
            os.mkdir('prizes')
        if not os.path.exists(round_dir):
            os.mkdir(round_dir)

        self.__generate_raffle_forms(round_dir, round_name)
        self.__generate_prize_forms(round_dir, round_name)

    def __generate_raffle_forms(self, round_dir, round_name):
        """Generate the raffle forms."""

        # Get raffle prizes.
        prizes = RafflePrize.objects.filter(round_name=round_name,
                                            winner__isnull=False)
        for prize in prizes:
            # Render form
            contents = render_to_string('view_prizes/form.txt', {
                'raffle': True,
                'prize': prize,
                'round': round_name
            })

            # Write to file
            filename = 'raffle-%s-%s.txt' % (slugify(prize.title), prize.winner.username)
            f = open('%s/%s' % (round_dir, filename), 'w')
            f.write(contents)

    def __generate_prize_forms(self, round_dir, round_name):
        """Generate the prize forms."""
        prizes = Prize.objects.filter(
            Q(award_to='individual_team') | Q(award_to='individual_overall'),
            round_name=round_name,
        )

        round_name = round_name if round_name != 'Overall' else None
        # Need to calculate winners for each prize.
        for prize in prizes:
            if prize.award_to == 'individual_team':
                # Need to calculate team winners for each team.
                for team in Team.objects.all():
                    leader = team.points_leaders(1, round_name)[0].user
                    prize.winner = leader
                    contents = render_to_string('view_prizes/form.txt', {
                        'raffle': False,
                        'prize': prize,
                        'round': round_name,
                        })

                    filename = '%s-%s.txt' % (team.name, leader.username)
                    f = open('%s/%s' % (round_dir, filename), 'w')
                    f.write(contents)

            else:
                leader = Profile.points_leaders(1, round_name)[0].user
                prize.winner = leader
                contents = render_to_string('view_prizes/form.txt', {
                    'raffle': False,
                    'prize': prize,
                    'round': round_name,
                    })

                filename = 'overall-%s.txt' % leader.username
                f = open('%s/%s' % (round_dir, filename), 'w')
                f.write(contents)
