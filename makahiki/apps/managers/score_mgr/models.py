"""
score manager models
"""
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


def _get_rounds():
    """Retrieves the rounds from the competition settings in a format that
    can be used in the ScoreboardEntry model."""

    return ((key, key) for key in settings.COMPETITION_ROUNDS.keys())


class ScoreboardEntry(models.Model):
    """Defines a class that tracks the user's scores in the rounds of the
    competition."""

    profile = models.ForeignKey("player_mgr.Profile", editable=False)
    round_name = models.CharField(max_length="30", choices=_get_rounds(),
        editable=False)
    points = models.IntegerField(default=0, editable=False)
    last_awarded_submission = models.DateTimeField(null=True, blank=True,
        editable=False)

    class Meta:
        """meta"""
        unique_together = (("profile", "round_name",),)
        ordering = ("round_name",)

    @staticmethod
    def user_round_overall_rank(user, round_name):
        """user round overall rank"""
        entry, _ = ScoreboardEntry.objects.get_or_create(
            profile=user.get_profile(),
            round_name=round_name
        )

        # Check if the user has done anything.
        if entry.last_awarded_submission:
            return ScoreboardEntry.objects.filter(
                Q(points__gt=entry.points) |
                Q(points=entry.points,
                    last_awarded_submission__gt=entry.last_awarded_submission),
                round_name=round_name,
            ).count() + 1

        # Users who have not done anything yet are assumed to be last.
        return ScoreboardEntry.objects.filter(
            points__gt=entry.points,
            round_name=round_name,
        ).count() + 1

    @staticmethod
    def user_round_team_rank(user, round_name):
        """user round team rank"""
        team = user.get_profile().team
        entry, _ = ScoreboardEntry.objects.get_or_create(
            profile=user.get_profile(),
            round_name=round_name
        )

        if entry.last_awarded_submission:
            return ScoreboardEntry.objects.filter(
                Q(points__gt=entry.points) |
                Q(points=entry.points,
                    last_awarded_submission__gt=entry.last_awarded_submission),
                profile__team=team,
                round_name=round_name,
            ).count() + 1
        else:
            return ScoreboardEntry.objects.filter(
                points__gt=entry.points,
                profile__team=team,
                round_name=round_name,
            ).count() + 1


class PointsTransaction(models.Model):
    """
    Entries that track points awarded to users.
    """
    user = models.ForeignKey(User)
    points = models.IntegerField()
    submission_date = models.DateTimeField()
    message = models.CharField(max_length=255)
    object_id = models.PositiveIntegerField(null=True)
    content_type = models.ForeignKey(ContentType, null=True)
    related_object = generic.GenericForeignKey("content_type", "object_id")

    @staticmethod
    def get_transaction_for_object(related_object, points):
        """get transaction log"""
        try:
            content_type = ContentType.objects.get_for_model(related_object)
            return PointsTransaction.objects.filter(
                points=points,
                object_id=related_object.id,
                content_type=content_type,
            )[0]

        except IndexError:
            return None
