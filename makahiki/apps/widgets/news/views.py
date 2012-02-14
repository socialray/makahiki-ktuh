import simplejson as json

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User

from managers.team_mgr.models import Post
from widgets.smartgrid import get_available_events, get_current_commitment_members, get_popular_tasks
from managers.player_mgr.models import Profile
from widgets.news.forms import WallForm
from widgets.smartgrid.forms import EventCodeForm

from widgets.news import DEFAULT_POST_COUNT

def supply(request):
    floor_id = request.user.get_profile().floor_id

    # Get floor posts.
    posts = Post.objects.filter(
        floor=floor_id
    ).order_by("-id").select_related('user__profile')

    post_count = posts.count
    posts = posts[:DEFAULT_POST_COUNT]
    is_more_posts = True if post_count > DEFAULT_POST_COUNT else False

    # Get upcoming events.
    events = get_available_events(request.user)

    # Get the user's current commitments.
    commitment_members = get_current_commitment_members(request.user).select_related("commitment")

    # Get the floor members.
    members = Profile.objects.filter(floor=floor_id).order_by(
        "-points",
        "-last_awarded_submission"
    ).select_related('user')[:12]

    form = EventCodeForm()

    return {
        "posts": posts,
        "events": events,
        "wall_form": WallForm(),
        "more_posts": is_more_posts,
        "commitment_members": commitment_members,
        "floor_members": members,
        "popular_tasks": get_popular_tasks(),
        "event_form": form,
        }


@never_cache
@login_required
def floor_members(request):
    members = User.objects.filter(profile__floor=request.user.get_profile().floor).order_by(
        "-profile__points",
        "-profile__last_awarded_submission",
    )

    return render_to_response("news/directory/floor_members.html", {
        "floor_members": members,
        }, context_instance=RequestContext(request))


@login_required
def post(request):
    if request.is_ajax() and request.method == "POST":
        form = WallForm(request.POST)
        if form.is_valid():
            wall_post = Post(
                user=request.user,
                floor=request.user.get_profile().floor,
                text=form.cleaned_data["post"]
            )
            wall_post.save()

            # Render the post and send it as a response.
            template = render_to_string("news/user_post.html", {"post": wall_post},
                context_instance=RequestContext(request))
            return HttpResponse(json.dumps({
                "contents": template,
                }), mimetype="application/json")

        # At this point there is a form validation error.
        return HttpResponse(json.dumps({
            "message": "This should not be blank."
        }), mimetype="application/json")

    raise Http404


@login_required
def more_posts(request):
    if request.is_ajax():
        floor = request.user.get_profile().floor
        if request.GET.has_key("last_post"):
            posts = Post.objects.filter(floor=floor, id__lt=int(request.GET["last_post"])).order_by(
                "-id")
        else:
            posts = Post.objects.filter(floor=floor).order_by("-id")

        post_count = posts.count
        posts = posts[:DEFAULT_POST_COUNT]
        is_more_posts = True if post_count > DEFAULT_POST_COUNT else False

        view_objects = {}
        view_objects["news"] = {"posts": posts,
                                "wall_form": WallForm(),
                                "more_posts": is_more_posts, }

        template = render_to_string("news/news_posts.html", {
            "view_objects": view_objects,
            }, context_instance=RequestContext(request))

        return HttpResponse(json.dumps({
            "contents": template,
            }), mimetype='application/json')

    raise Http404