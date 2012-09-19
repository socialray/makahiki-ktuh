"""participation game related functions."""
from apps.managers.cache_mgr import cache_mgr
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.team_mgr import team_mgr
from apps.widgets.participation.models import ParticipationSetting, TeamParticipation


def award_participation():
    """award the participation rate for all team."""

    if not challenge_mgr.is_game_enabled("Participation Game"):
        return

    p_setting, _ = ParticipationSetting.objects.get_or_create(pk=1)

    for team in team_mgr.team_active_participation():
        team_participation, _ = TeamParticipation.objects.get_or_create(team=team)

        # check if the participation rate change
        if team_participation.participation != team.active_participation:
            # save the new participation rate

            if team.active_participation == 100:
                if team_participation.awarded_percent != "100":
                    team_participation.awarded_percent = "100"
                    team_mgr.award_member_points(team,
                                             p_setting.points_100_percent,
                                             "Team 100% participation")
            elif team.active_participation >= 75:
                if team_participation.awarded_percent != "75":
                    team_participation.awarded_percent = "75"
                    team_mgr.award_member_points(team,
                                             p_setting.points_75_percent,
                                             "Team 75% participation")
            elif team.active_participation >= 50:
                if not team_participation.awarded_percent:
                    team_participation.awarded_percent = "50"
                    team_mgr.award_member_points(team,
                                             p_setting.points_50_percent,
                                             "Team 50% participation")

            team_participation.participation = team.active_participation
            team_participation.save()
            cache_mgr.delete("team_participation")
