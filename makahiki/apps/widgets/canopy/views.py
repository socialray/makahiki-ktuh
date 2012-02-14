import simplejson as json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache
from django.db.models import Q

from widgets.canopy.models import Mission, Post, MissionMember
from managers.player_mgr.models import Profile
from widgets.canopy.decorators import can_access_canopy
from widgets.canopy.forms import WallForm
from managers.team_mgr.models import Team, Dorm

# Number of posts to load at a time.

DEFAULT_POST_COUNT = 10

@login_required
@never_cache
@can_access_canopy
def index(request):
    view_objects = {}
    view_objects["canopy"] = supply(request)

    return render_to_response("canopy.html", {
        "view_objects": view_objects,
        }, context_instance=RequestContext(request))


def supply(request):
    """
    Directs the user to the canopy page.
    """
    # Load quests
    canopy_missions = Mission.objects.all()

    # Load wall
    form = WallForm()
    posts = Post.objects.order_by("-id").select_related('user')
    post_count = posts.count()
    posts = posts[:DEFAULT_POST_COUNT]
    is_more_posts = True if post_count > DEFAULT_POST_COUNT else False

    # Load members
    canopy_members = User.objects.filter(
        Q(is_superuser=True) | Q(is_staff=True) | Q(profile__canopy_member=True)
    ).select_related('profile')

    # Load canopy karma scoreboard.
    karma_scoreboard = Profile.objects.filter(
        canopy_member=True,
    ).order_by("-canopy_karma")[:10]

    # Check for the about cookie.
    hide_about = False
    if request.COOKIES.has_key("hide-about"):
        hide_about = True

    viz = request.REQUEST.get("viz", None)

    all_lounges = Team.objects.order_by('name').all()
    all_dorms = Dorm.objects.order_by('name').all()

    for dorm in all_dorms:
        dorm.teams = dorm.team_set.order_by('-name').all()

    if request.user.get_profile().team:
        dorm_lounges = request.user.get_profile().team.dorm.team_set.all()
    else:
        dorm_lounges = all_lounges[:5]

    return  {
        "in_canopy": True,
        "canopy_missions": canopy_missions,
        "wall_form": form,
        "posts": posts,
        "more_posts": is_more_posts,
        "members": canopy_members,
        "hide_about": hide_about,
        "viz": viz,
        "karma_scoreboard": karma_scoreboard,
        "all_lounges": all_lounges,
        "dorm_lounges": dorm_lounges,
        "all_dorms": all_dorms,
        }

### User methods -------------------------
@login_required
@never_cache
@can_access_canopy
def members(request):
    """
    Lists all of the members of the canopy.
    """
    canopy_missions = Mission.objects.all()
    canopy_members = User.objects.filter(
        Q(is_superuser=True) | Q(is_staff=True) | Q(profile__canopy_member=True))

    return render_to_response("canopy/directory/members.html", {
        "in_canopy": True,
        "canopy_missions": canopy_missions,
        "members": canopy_members,
        }, context_instance=RequestContext(request))

### Quest methods -------------------------
@login_required
@can_access_canopy
def mission_accept(request, slug):
    if request.method == "POST":
        user = request.user
        mission = get_object_or_404(Mission, slug=slug)
        if user not in mission.users.all():
            MissionMember.objects.create(
                mission=mission,
                user=user,
            )

        return HttpResponseRedirect(reverse("canopy_index"))

    raise Http404


@login_required
@can_access_canopy
def mission_cancel(request, slug):
    if request.method == "POST":
        user = request.user
        member = get_object_or_404(MissionMember,
            mission__slug=slug,
            user=user,
            completed=False,
        )
        member.delete()

        return HttpResponseRedirect(reverse("canopy_index"))

    raise Http404

### Wall methods -------------------------

@login_required
@can_access_canopy
def post(request):
    if request.method == "POST":
        form = WallForm(request.POST)
        if form.is_valid(): # Should always be valid. Check for content is done on client side.
            wall_post = Post(
                user=request.user,
                text=form.cleaned_data["post"],
            )
            wall_post.save()

            if request.is_ajax():
                # Render the post and send it as a response.
                template = render_to_string("canopy/post.html", {"post": wall_post},
                    context_instance=RequestContext(request))
                return HttpResponse(json.dumps({
                    "contents": template,
                    }), mimetype="application/json")
            else:
                return HttpResponseRedirect(reverse("canopy_index"))

    raise Http404


@login_required
@can_access_canopy
def more_posts(request):
    if request.is_ajax():
        if request.GET.has_key("last_post"):
            posts = Post.objects.filter(id__lt=int(request.GET["last_post"])).order_by("-id")
        else:
            posts = Post.objects.order_by("-id")

        post_count = posts.count()
        posts = posts[:DEFAULT_POST_COUNT]
        is_more_posts = True if post_count > DEFAULT_POST_COUNT else False

        template = render_to_string("canopy/wall_posts.html", {
            "posts": posts,
            "more_posts": is_more_posts,
            }, context_instance=RequestContext(request))

        return HttpResponse(json.dumps({
            "contents": template,
            }), mimetype='application/json')

    raise Http404
  