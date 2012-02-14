import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import F
from django.db.models.aggregates import Count
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.cache import never_cache

from managers.base_mgr import get_round_info
from managers.team_mgr.models import Post
from widgets.energy import generate_chart_url
from widgets.energy.forms import EnergyGoalVotingForm
from widgets.energy.models import TeamEnergyGoal, EnergyGoal, EnergyGoalVote
from widgets.news.forms import WallForm

import simplejson as json
from widgets.smartgrid import get_available_golow_activities

@login_required
@never_cache
def index(request):
    view_objects = {}
    view_objects["energy"] = supply(request)

    return render_to_response("energy.html", {
        "view_objects": view_objects,
        }, context_instance=RequestContext(request))


def supply(request):
    user = request.user
    team = user.get_profile().team
    golow_activities = get_available_golow_activities(user)
    golow_posts = Post.objects.filter(team=team, style_class="user_post").select_related(
        'user__profile').order_by("-id")[:5]

    rounds = get_round_info()
    scoreboard_rounds = []
    today = datetime.datetime.today()
    for key in rounds.keys():
        # Check if this round happened already or if it is in progress.
        # We don't care if the round happens in the future.
        if today >= datetime.datetime.strptime(rounds[key]["start"], "%Y-%m-%d"):
            scoreboard_rounds.append(key)

    # Generate the scoreboard for energy goals.
    # We could aggregate the energy goals in teams, but there's a bug in Django.
    # See https://code.djangoproject.com/ticket/13461
    goals_scoreboard = TeamEnergyGoal.objects.filter(
        actual_usage__lte=F("goal_usage")
    ).values(
        "team__number",
        "team__dorm__name"
    ).annotate(completions=Count("team")).order_by("-completions")

    return {
        "team": team,
        "scoreboard_rounds": scoreboard_rounds,
        "golow_activities": golow_activities,
        "posts": golow_posts,
        "wall_form": WallForm(),
        "goals_scoreboard": goals_scoreboard,
        }


def vote(request, goal_id):
    """Adds the user's vote to the goal."""
    if request.method != "POST":
        return Http404

    goal = get_object_or_404(EnergyGoal, pk=goal_id)
    user = request.user

    form = EnergyGoalVotingForm(request.POST, instance=EnergyGoalVote(user=user, goal=goal))
    if form.is_valid():
        form.save()
        messages.info(request, 'Thank you for your vote!')

    if request.META.has_key("HTTP_REFERER"):
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    else:
        return HttpResponseRedirect(reverse("profile_detail", args=(user.pk,)))


def voting_results(request, goal_id):
    """Get the voting results for the user's team."""
    goal = get_object_or_404(EnergyGoal, pk=goal_id)

    profile = request.user.get_profile()
    results = goal.get_team_results(profile.team)
    url = generate_chart_url(results)

    return HttpResponse(json.dumps({
        "results": list(results), # Needed to convert results from a queryset.
        "url": url,
        }), mimetype='application/json')

  