"""Implements the quest widget."""
from apps.managers.cache_mgr import cache_mgr
from apps.managers.challenge_mgr import challenge_mgr

from apps.widgets.quests import MAX_AVAILABLE_QUESTS

from apps.widgets.quests.models import Quest, QuestMember
from apps.widgets.notifications.models import UserNotification


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


def get_quests_from_cache(user):
    """
    get the quests for the user and store in cache.
    """
    if not challenge_mgr.is_game_enabled("Quest Game Mechanics"):
        return {}

    return_dict = cache_mgr.get_cache("get_quests-%s" % user.username)
    if return_dict is None:
        return_dict = get_quests(user)
        cache_mgr.set_cache("get_quests-%s" % user.username, return_dict, 1800)
    return return_dict


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
    for quest in Quest.objects.exclude(questmember__user=user).order_by('priority'):
        if quest.can_add_quest(user) and not quest.completed_quest(user):
            quests.append(quest)

            if len(quests) == num_quests:
                return quests

    return quests
