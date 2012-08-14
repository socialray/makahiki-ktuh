"""participation game related functions."""
from apps.managers.team_mgr import team_mgr
from apps.widgets.participation.models import ParticipationSetting, TeamParticipation


def award_participation():
    """award the participation rate for all team."""
    p_setting, _ = ParticipationSetting.objects.get_or_create(pk=1)
    for team in team_mgr.team_active_participation():
        team_participation, _ = TeamParticipation.objects.get_or_create(team=team)

        # check if the participation rate change
        if team_participation.participation != team.active_participation:
            # save the new participation rate
            team_participation.participation = team.active_participation
            team_participation.save()

            if team.active_participation == 100:
                team_mgr.award_member_points(team,
                                             p_setting.points_100_percent,
                                             "Team 100% participation")
            elif team.active_participation >= 75:
                team_mgr.award_member_points(team,
                                             p_setting.points_75_percent,
                                             "Team 75% participation")
            elif team.active_participation >= 50:
                team_mgr.award_member_points(team,
                                             p_setting.points_50_percent,
                                             "Team 50% participation")
