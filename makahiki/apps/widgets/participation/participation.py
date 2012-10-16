"""participation game related functions."""
from apps.managers.cache_mgr import cache_mgr
from django.template.defaultfilters import slugify
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.team_mgr import team_mgr
from apps.managers.team_mgr.models import Team
from apps.widgets.participation.models import ParticipationSetting, TeamParticipation


def participation_ranks(round_name):
    """Generate the scoreboard for participation game."""
    cache_key = "p_ranks-%s" % slugify(round_name)
    p_ranks = cache_mgr.get_cache(cache_key)
    if p_ranks is None:
        p_settings, _ = ParticipationSetting.objects.get_or_create(pk=1)
        p_ranks = {
            "participation_100": [],
            "participation_75": [],
            "participation_50": [],
            "participation_0": [],
            "p_settings": p_settings}
        team_participation = TeamParticipation.objects.filter(
            round_name=round_name).select_related("team")

        if not team_participation:
            team_participation = Team.objects.all()
            for p in team_participation:
                p.team = p
                p.participation = 0
                p_ranks["participation_0"].append(p)
        else:
            for p in team_participation:
                if p.participation >= 100:
                    p_ranks["participation_100"].append(p)
                elif p.participation >= 75:
                    p_ranks["participation_75"].append(p)
                elif p.participation >= 50:
                    p_ranks["participation_50"].append(p)
                else:
                    p_ranks["participation_0"].append(p)  # less than 50
        cache_mgr.set_cache(cache_key, p_ranks, 3600)
    return p_ranks


def award_participation():
    """award the participation rate for all team."""

    if not challenge_mgr.is_game_enabled("Participation Game"):
        return

    p_setting, _ = ParticipationSetting.objects.get_or_create(pk=1)

    current_round = challenge_mgr.get_round_name()

    for team in team_mgr.team_active_participation(round_name=current_round):
        team_participation, _ = TeamParticipation.objects.get_or_create(
            team=team, round_name=current_round)

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

    # store the overall participation rate
    for team in team_mgr.team_active_participation(round_name="Overall"):
        team_participation, _ = TeamParticipation.objects.get_or_create(
            team=team, round_name="Overall")
        # check if the participation rate change
        if team_participation.participation != team.active_participation:
            # save the new participation rate
            team_participation.participation = team.active_participation
            team_participation.save()
