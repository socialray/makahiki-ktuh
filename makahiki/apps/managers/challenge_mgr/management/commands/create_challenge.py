"""Invocation:  python manage.py create_challenge

Create a challenge site with the specified site_name."""
from django.core import management
from apps.managers.challenge_mgr.models import ChallengeSetting


class Command(management.base.BaseCommand):
    """command"""
    help = 'create a challenge site with the specified site_name. Usage: create <site_name>'

    def handle(self, *args, **options):
        """handle create a challenge site"""
        if len(args) == 0:
            self.stdout.write("Please specify site_name.")
            return

        site_name = args[0]
        challenges = ChallengeSetting.objects.all()
        if challenges:
            print "Can not create the challenge. A challenge with site name '%s' exists. " \
            "Please use admin interface to change the name. " % challenges[0].site_name
        else:
            ChallengeSetting(site_name=site_name).save()
            print "challenge site %s created." % site_name
