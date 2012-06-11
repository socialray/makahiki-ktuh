"""action_feedback model."""

from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

from apps.widgets.smartgrid.models import Action


class ActionFeedback(models.Model):
    """Defines the Action Feedback model."""
    action = models.ForeignKey(Action,
                               null=True, blank=True,
                               help_text="The action this feedback is for.")
    user = models.ForeignKey(User,
                             null=True, blank=True,
                             help_text="The user providing the feedback.")
    rating = models.IntegerField(help_text="The user's rating of the action.")
    comment = models.CharField(
                               max_length=1500,
                               blank=True,
                               null=True,
                               help_text="The user's comments about the action.")
    added = models.DateTimeField(editable=False, help_text="The time the feedback was made.")
    changed = models.DateTimeField(editable=False, help_text="The time the feedback was changed.")

    def __unicode__(self):
        return self.user.name + " rated " + self.action.name + ": " + self.rating + " " + self.comment
