"""
team mgr models
"""
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models import Sum, Max

from managers.settings_mgr import get_current_round

# Create your models here.

class Group(models.Model):
    """
    defines the group that a team belongs to.
    """
    # Automatically populate slug field when the name is added.
    prepopulated_fields = {"slug": ("name",)}

    name = models.CharField(max_length=200, help_text="The name of the group.")
    slug = models.SlugField(max_length=20,
        help_text="Automatically generated if left blank.")

    def __unicode__(self):
        return self.name

    def team_points_leaders(self, num_results=10, round_name=None):
        """
        Returns the top points leaders for the given group.
        """
        if round_name:
            return self.team_set.filter(
                profile__scoreboardentry__round_name=round_name
            ).annotate(
                points=Sum("profile__scoreboardentry__points"),
                last=Max("profile__scoreboardentry__last_awarded_submission")
            ).order_by("-points", "-last")[:num_results]

        return self.team_set.annotate(
            points=Sum("profile__points"),
            last=Max("profile__last_awarded_submission")
        ).order_by("-points", "-last")[:num_results]

    def save(self, *args, **kwargs):
        """Custom save method to generate slug and set created_at/updated_at."""
        if not self.slug:
            self.slug = slugify(self.name)

        super(Group, self).save(*args, **kwargs)


class Team(models.Model):
    """
    represents a team that a player belongs to.
    """
    prepopulated_fields = {"slug": ("name",)}

    name = models.CharField(
        help_text="The team name",
        max_length=50)
    slug = models.SlugField(max_length=50,
        help_text="Automatically generated if left blank.")
    group = models.ForeignKey(Group, help_text="The group this team belongs to.")

    def __unicode__(self):
        return self.name

    @staticmethod
    def team_points_leaders(num_results=10, round_name=None):
        """
        Returns the team points leaders across all groups.
        """
        if round_name:
            return Team.objects.select_related('group').filter(
                profile__scoreboardentry__round_name=round_name
            ).annotate(
                points=Sum("profile__scoreboardentry__points"),
                last=Max("profile__scoreboardentry__last_awarded_submission")
            ).order_by("-points", "-last")[:num_results]

        return Team.objects.select_related('group').annotate(
            points=Sum("profile__points"),
            last=Max("profile__last_awarded_submission")
        ).order_by("-points", "-last")[:num_results]

    def points_leaders(self, num_results=10, round_name=None):
        """
        Gets the individual points leaders for the team.
        """
        if round_name:
            return self.profile_set.select_related('scoreboardentry').filter(
                scoreboardentry__round_name=round_name
            ).order_by("-scoreboardentry__points",
                "-scoreboardentry__last_awarded_submission", )[:num_results]

        return self.profile_set.all().order_by("-points", "-last_awarded_submission")[:num_results]

    def current_round_rank(self):
        """ current round rank
        """
        current_round = get_current_round()
        if current_round:
            return self.rank(round_name=current_round)

        return None

    def rank(self, round_name=None):
        """Returns the rank of the team across all groups."""
        if round_name:
            from managers.score_mgr.models import ScoreboardEntry

            aggregate = ScoreboardEntry.objects.filter(
                profile__team=self,
                round_name=round_name
            ).aggregate(points=Sum("points"),
                last=Max("last_awarded_submission"))

            points = aggregate["points"] or 0
            last_awarded_submission = aggregate["last"]
            # Group by teams, filter out other rounds, and annotate.
            annotated_teams = ScoreboardEntry.objects.values(
                "profile__team").filter(
                round_name=round_name
            ).annotate(
                team_points=Sum("points"),
                last_awarded=Max("last_awarded_submission")
            )
        else:
            aggregate = self.profile_set.aggregate(points=Sum("points"),
                last=Max("last_awarded_submission"))
            points = aggregate["points"] or 0
            last_awarded_submission = aggregate["last"]

            annotated_teams = Team.objects.annotate(
                team_points=Sum("profile__points"),
                last_awarded_submission=Max("profile__last_awarded_submission")
            )

        count = annotated_teams.filter(team_points__gt=points).count()
        # If there was a submission, tack that on to the count.
        if last_awarded_submission:
            count = count + annotated_teams.filter(
                team_points=points,
                last_awarded_submission__gt=last_awarded_submission
            ).count()

        return count + 1

    def current_round_points(self):
        """Returns the number of points for the current round."""
        current_round = get_current_round()
        if current_round:
            return self.points(round_name=current_round)

        return None

    def points(self, round_name=None):
        """Returns the total number of points for the team.  Takes an optional parameter for a
        round."""
        if round_name:
            from managers.player_mgr.models import ScoreboardEntry

            dictionary = ScoreboardEntry.objects.filter(profile__team=self,
                round_name=round_name).aggregate(Sum("points"))
        else:
            dictionary = self.profile_set.aggregate(Sum("points"))

        return dictionary["points__sum"] or 0

    def save(self, *args, **kwargs):
        """Custom save method to generate slug and set created_at/updated_at."""
        if not self.slug:
            self.slug = slugify(self.name)

        super(Team, self).save(*args, **kwargs)


class Post(models.Model):
    """Represents a wall post on a user's wall."""
    user = models.ForeignKey(User)
    team = models.ForeignKey(Team)
    text = models.TextField()
    style_class = models.CharField(max_length=50,
        default="user_post") #CSS class to apply to this post.
    created_at = models.DateTimeField(editable=False)

    def __unicode__(self):
        return "%s (%s): %s" % (self.team, self.user.username, self.text)

    def date_string(self):
        """Formats the created date into a pretty string."""
        return self.created_at.strftime("%m/%d %I:%M %p")

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.today()

        super(Post, self).save(*args, **kwargs)


class PostComment(models.Model):
    """represent the structure for comments in a post"""
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    text = models.TextField()
    created_at = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.date.today()

        super(PostComment, self).save(*args, **kwargs)