import datetime

from widgets.energy.models import EnergyGoal, EnergyGoalVote, TeamEnergyGoal
from widgets.energy.forms import EnergyGoalVotingForm

from managers.team_mgr.models import Team

def get_info_for_user(user):
    """Generates a return dictionary for use in rendering the user profile."""
    current_goal = EnergyGoal.get_current_goal()
    if current_goal:
        in_voting = current_goal.in_voting_period()
        can_vote = in_voting and current_goal.user_can_vote(user)
        if can_vote:
            form = EnergyGoalVotingForm(
                instance=EnergyGoalVote(user=user, goal=current_goal,
                    percent_reduction=current_goal.default_goal)
            )

            return {
                "goal": current_goal,
                "form": form,
                }
        elif in_voting:
            profile = user.get_profile()
            results = current_goal.get_team_results(profile.team)
            results_url = generate_chart_url(results)
            return {
                "goal": current_goal,
                "results_url": results_url,
                }

        else:
            team = user.get_profile().team
            try:
                team_goal = team.teamenergygoal_set.get(goal=current_goal)
                return {
                    "goal": current_goal,
                    "team_goal": team_goal,
                    }
            except TeamEnergyGoal.DoesNotExist:
                pass

    return None


def generate_chart_url(results):
    """Helper method to generate a chart url given the goal's voting results."""
    # Create base url.
    base_url = "http://chart.apis.google.com/chart?cht=bhs&chs=150x100&chxt=x,y&chtt=Voting%20Results"

    # Construct the data and label parameters
    data = "&chd=t:"
    label = "&chxl=1:"
    max_votes = 0
    for result in results:
        if result["votes"] > max_votes:
            max_votes = result["votes"]

        label += "|%d%%" % result["percent_reduction"]
        data += "%d," % result["votes"]

    # Remove last comma from the data parameter.
    data = data[0:len(data) - 1]

    # Add range parameter.
    data_range = "&chxr=0,0,%d&chds=0,%d" % (max_votes, max_votes)

    # Add background color parameter.
    bg_color = "&chf=bg,s,F5F3E5"

    # Add data color.
    data_color = "&chco=459E00"

    return base_url + data + label + data_range + bg_color + data_color


def generate_team_goals():
    """Called by a cron task to generate the team goals for a team."""
    goal = EnergyGoal.get_current_goal()
    today = datetime.date.today()
    if goal and goal.voting_end_date <= today and goal.teamenergygoal_set.count() == 0:
        # Go through the votes and create energy goals for the team.
        for team in Team.objects.all():
            results = goal.get_team_results(team)
            percent_reduction = 0
            if len(results) > 0:
                percent_reduction = results[0]["percent_reduction"]

            team_goal = TeamEnergyGoal(team=team, goal=goal,
                percent_reduction=percent_reduction)
            team_goal.save()