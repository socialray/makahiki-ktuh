"""action_feedback model."""

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
    rating = models.IntegerField(help_text="The user's rating of the action.", default=0)
    comment = models.CharField(
                               max_length=1500,
                               blank=True,
                               null=True,
                               help_text="The user's comments about the action.")
    added = models.DateTimeField(editable=False,
                                 help_text="The time the feedback was made.",
                                 auto_now_add=True)
    changed = models.DateTimeField(editable=False,
                                   help_text="The time the feedback was changed.",
                                   auto_now=True)

    def __unicode__(self):
        return "%s rated %s %d and said %s" % \
            (self.user.username, self.action.name, self.rating, self.comment)
