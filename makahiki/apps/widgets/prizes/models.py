from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from managers.base_mgr import get_round_info
from managers.player_mgr.models import Profile
from managers.team_mgr.models import Dorm, Team

class Prize(models.Model):
    """
    Represents a prize in the system.
    """
    ROUND_CHOICES = ((round_name, round_name) for round_name in get_round_info().keys())
    AWARD_TO_CHOICES = (
        ("individual_overall", "Individual (Overall)"),
        ("individual_team", "Individual (" + settings.COMPETITION_GROUP_NAME + ")"),
        # ("individual_dorm", "Individual (Dorm)"),
        ("team_overall", settings.COMPETITION_GROUP_NAME + " (Overall)"),
        ("team_dorm", settings.COMPETITION_GROUP_NAME + " (Dorm)"),
        # ("dorm", "Dorm"), # Not implemented yet.
        )
    AWARD_CRITERIA_CHOICES = (
        ("points", "Points"),
        ("energy", "Energy")
        )

    title = models.CharField(max_length=30, help_text="The title of your prize.")
    short_description = models.TextField(
        help_text="Short description of the prize. This should include information about who can win it."
    )
    long_description = models.TextField(
        help_text="Additional details about the prize."
    )
    value = models.IntegerField(help_text="The value of the prize.")
    image = models.ImageField(
        max_length=1024,
        upload_to="prizes",
        blank=True,
        help_text="A picture of your prize."
    )
    round_name = models.CharField(
        max_length=20,
        choices=ROUND_CHOICES,
        help_text="The round in which this prize can be won."
    )
    award_to = models.CharField(
        max_length=20,
        choices=AWARD_TO_CHOICES,
        help_text="Who the prize is awarded to.  This is used to calculate who's winning."
    )
    competition_type = models.CharField(
        max_length=20,
        choices=AWARD_CRITERIA_CHOICES,
        help_text="The 'competition' this prize is awarded to.")

    def __unicode__(self):
        return self.round_name + ": " + self.title

    class Meta:
        unique_together = ("round_name", "award_to", "competition_type")

    def num_awarded(self, team=None):
        """
        Returns the number of prizes that will be awarded for this prize.
        """
        _ = team
        if self.award_to in ("individual_overall", "team_overall", "dorm"):
            # For overall prizes, it is only possible to award one.
            return 1

        elif self.award_to in ("team_dorm", "individual_dorm"):
            # For dorm prizes, this is just the number of dorms.
            return Dorm.objects.count()

        elif self.award_to == "individual_team":
            # This is awarded to each team.
            return Team.objects.count()

        raise Exception("Unknown award_to value '%s'" % self.award_to)

    def leader(self, team=None):
        if self.competition_type == "points":
            return self._points_leader(team)
        else:
            return self._energy_leader(team)

    def _points_leader(self, team=None):
        round_name = None if self.round_name == "Overall" else self.round_name
        if self.award_to == "individual_overall":
            return Profile.points_leaders(num_results=1, round_name=round_name)[0]

        elif self.award_to == "team_dorm":
            return team.dorm.team_points_leaders(num_results=1, round_name=round_name)[0]

        elif self.award_to == "team_overall":
            return Team.team_points_leaders(num_results=1, round_name=round_name)[0]

        elif self.award_to == "individual_team":
            if team:
                return team.points_leaders(num_results=1, round_name=round_name)[0]
            return None

        raise Exception("'%s' is not implemented yet." % self.award_to)

    def _energy_leader(self, team):
        _ = team
        raise Exception(
            "Energy leader information is not implemented here.  Needs to be implemented at view/controller layer.")


class RaffleDeadline(models.Model):
    ROUND_CHOICES = ((round_name, round_name) for round_name in get_round_info().keys())

    round_name = models.CharField(
        max_length=20,
        choices=ROUND_CHOICES,
        help_text="The round in which this prize can be won.",
        unique=True,
    )
    pub_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __unicode__(self):
        return "%s deadline" % self.round_name


class RafflePrize(models.Model):
    ROUND_CHOICES = ((round_name, round_name) for round_name in get_round_info().keys())

    title = models.CharField(max_length=30, help_text="The title of your prize.")
    value = models.IntegerField(help_text="The value of your prize")
    description = models.TextField(
        help_text="Description of the prize.  Uses <a href='http://daringfireball.net/projects/markdown/syntax'>Markdown</a> formatting."
    )
    image = models.ImageField(
        max_length=1024,
        upload_to="prizes",
        blank=True,
        help_text="A picture of your prize."
    )
    deadline = models.ForeignKey(RaffleDeadline)
    winner = models.ForeignKey(User, null=True, blank=True)

    def __unicode__(self):
        return "%s: %s" % (self.deadline.round_name, self.title)

    def add_ticket(self, user):
        """
        Adds a ticket from the user if they have one.  Throws an exception if they cannot add a ticket.
        """
        profile = user.get_profile()
        if profile.available_tickets() <= 0:
            raise Exception("This user does not have any tickets to allocate.")

        ticket = RaffleTicket(raffle_prize=self, user=user)
        ticket.save()

    def remove_ticket(self, user):
        """
        Removes an allocated ticket.
        """
        # Get the first ticket that matches the query.
        ticket = RaffleTicket.objects.filter(raffle_prize=self, user=user)[0]
        ticket.delete()

    def allocated_tickets(self, user=None):
        """
        Returns the number of tickets allocated to this prize.
        Takes an optional argument to return the number of tickets allocated by the user.
        """
        query = self.raffleticket_set.filter(raffle_prize=self)
        if user:
            query = query.filter(user=user)

        return query.count()


class RaffleTicket(models.Model):
    user = models.ForeignKey(User)
    raffle_prize = models.ForeignKey(RafflePrize)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
