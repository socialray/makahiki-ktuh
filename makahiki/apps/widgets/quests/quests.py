"""Implements the quest widget."""
from apps.managers.score_mgr import score_mgr
from apps.utils import utils
from apps.widgets.quests import MAX_AVAILABLE_QUESTS

from apps.widgets.quests.models import Quest, QuestMember
from apps.widgets.notifications.models import UserNotification
from apps.widgets.smartgrid import smartgrid


def has_points(user, points, round_name="Overall"):
    """Returns True if the user has at least the requested number of points."""
    return score_mgr.player_has_points(user.get_profile(), points, round_name)


def has_action(user, slug=None, name=None, action_type=None):
    """Determines if the user is participating in a task."""
    return smartgrid.has_action(user, slug, name, action_type)


def completed_action(user, slug=None, action_type=None):
    """Determines if the user has completed the named task or completed a task of the given type."""
    return smartgrid.completed_action(user, slug, action_type)


def num_actions_completed(user, num_tasks, category_name=None, action_type=None):
    """Returns True if the user has completed the requested number of tasks."""
    return smartgrid.num_actions_completed(user, num_tasks, category_name, action_type)


def allocated_ticket(user):
    """Returns True if the user has any allocated tickets."""
    return user.raffleticket_set.count() > 0


def badge_awarded(user, badge_slug):
    """Returns True if the badge is awarded to the user."""
    for badge in user.badges_earned.all():
        if badge.slug == badge_slug:
            return True

    return False


def posted_to_wall(user):
    """Returns True if the user posted to their wall and False otherwise."""
    if user.post_set.filter(style_class="user_post").count() > 0:
        return True
    return False


def set_profile_pic(user):
    """Returns True if the user posted to their wall and False otherwise."""
    if user.avatar_set.filter(primary=True).count() > 0:
        return True
    return False

CONDITIONS = {
    "has_action": has_action,
    "completed_action": completed_action,
    "has_points": has_points,
    "allocated_ticket": allocated_ticket,
    "num_actions_completed": num_actions_completed,
    "badge_awarded": badge_awarded,
    "posted_to_wall": posted_to_wall,
    "set_profile_pic": set_profile_pic,
    }


def process_conditions_string(conditions_string, user):
    """Utility method to evaluate conditions."""
    return utils.eval_predicates(conditions_string, user, CONDITIONS)


def possibly_completed_quests(user):
    """Check if the user may have completed one of their quests.
       Returns an array of the completed quests."""
    user_quests = user.quest_set.filter(questmember__completed=False, questmember__opt_out=False)
    completed = []
    for quest in user_quests:
        if quest.completed_quest(user):
            member = QuestMember.objects.get(user=user, quest=quest)
            member.completed = True
            member.save()
            completed.append(quest)

            # Create quest notification.
            message = "Congratulations! You completed the '%s' quest." % quest.name
            UserNotification.create_success_notification(user, message, display_alert=True)

    return completed


def get_quests(user):
    """Loads the quests for the user.
       Returns a dictionary of two things:

         * The user's current quests (user_quests).
         * Quests the user can participate in (available_quests)."""
    return_dict = {}

    # Check for completed quests.
    possibly_completed_quests(user)

    # Load the user's quests
    quests = get_user_quests(user)
    return_dict.update({"user_quests": quests})

    # Check if the user can add more quests
    # Note that the second set of quests are not a queryset object.
    if (quests.count() < MAX_AVAILABLE_QUESTS):
        return_dict.update({
            "available_quests": get_available_quests(user, MAX_AVAILABLE_QUESTS - len(quests))})

    return return_dict


def get_user_quests(user):
    """Get the quests the user is participating in."""
    return user.quest_set.filter(
        questmember__user=user,
        questmember__opt_out=False,
        questmember__completed=False
    )


def get_available_quests(user, num_quests):
    """Get the quests the user could participate in."""
    quests = []
    for quest in Quest.objects.exclude(questmember__user=user).order_by('level'):
        if quest.can_add_quest(user):
            quests.append(quest)

            if len(quests) == num_quests:
                return quests

    return quests
