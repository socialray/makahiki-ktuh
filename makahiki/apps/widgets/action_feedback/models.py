"""action_feedback model."""

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

from apps.widgets.smartgrid.models import Action
from apps.managers.challenge_mgr import challenge_mgr
from apps.admin.admin import challenge_designer_site, challenge_manager_site, developer_site


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
    admin_tool_tip = "Player Feedback about Actions"

    def __unicode__(self):
        return "%s rated %s %d and said %s" % \
            (self.user.username, self.action.name, self.rating, self.comment)

admin.site.register(ActionFeedback)
challenge_designer_site.register(ActionFeedback)
challenge_manager_site.register(ActionFeedback)
developer_site.register(ActionFeedback)
challenge_mgr.register_developer_game_info_model("Smart Grid Game", ActionFeedback)
