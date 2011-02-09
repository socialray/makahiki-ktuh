import datetime
import simplejson as json

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.cache import never_cache
from django.db.models import Count

from pages.view_activities.forms import *
from components.activities.models import *
from components.activities import *
from components.floors.models import *
from components.floors import *
from components.makahiki_profiles.models import *
from components.makahiki_profiles import *

MAX_INDIVIDUAL_STANDINGS = 10
ACTIVITIES_COL_COUNT = 3

def index(request):
  user = request.user
  events = get_available_events(user)
  floor = user.get_profile().floor
  
  ordered_floors = Floor.objects.annotate(f_points=Sum("profile__points")).order_by("-f_points")
  ordered_all_profiles = Profile.objects.order_by("-points")
  ordered_floor_profiles = Profile.objects.filter(floor=floor).order_by("-points")
  standings = zip(ordered_floors,ordered_all_profiles,ordered_floor_profiles)[:MAX_INDIVIDUAL_STANDINGS]
  
  categories = Category.objects.annotate(total=Count("activity"),
        commitment_total=Count("commitment"), 
        point_total=Sum("activity__point_value"),
        commitment_point_total=Sum("commitment__point_value"),
        )
        
  ## construct the categories list as 2-dimension array
  categories_list = []
  cat_col_list = []
  col_count = 0
  for cat in categories:
    cat.total = cat.total + cat.commitment_total
    cat.locked = cat.id > 2
    if (cat.commitment_point_total == None):
      cat.commitment_point_total = 0
    if (cat.point_total == None):
      cat.point_total = 0  
    cat.point_total = cat.point_total + cat.commitment_point_total
    cat_col_list.append([cat, get_completed_tasks(user, cat), get_awarded_points(user,cat)])
    col_count = col_count + 1
    if col_count == ACTIVITIES_COL_COUNT:    	  		 	  
      categories_list.append(cat_col_list)
      cat_col_list = []
      col_count = 0
  		
  categories_list.append(cat_col_list)
  		  
  return render_to_response("view_activities/index.html", {
    "events": events,
    "profile":user.get_profile(),
    "floor": floor,
    "standings":standings,
    "categories":categories_list,
  }, context_instance=RequestContext(request))
    
@login_required
def view_codes(request, activity_id):
  """View the confirmation codes for a given activity."""
  
  if not request.user or not request.user.is_staff:
    raise Http404
    
  activity = get_object_or_404(Activity, pk=activity_id)
  codes = ConfirmationCode.objects.filter(activity=activity)
  if len(codes) == 0:
    raise Http404
  
  return render_to_response("view_activities/view_codes.html", {
    "activity": activity,
    "codes": codes,
  }, context_instance = RequestContext(request))

### Private methods.

def __add_commitment(request, commitment_id):
  """Commit the current user to the commitment."""
  
  commitment = get_object_or_404(Commitment, pk=commitment_id)
  user = request.user
  
  if not can_add_commitments(user):
    message = "You can only have %d active commitments." % MAX_COMMITMENTS
    user.message_set.create(message=message)
  elif commitment in get_current_commitments(user):
    user.message_set.create(message="You are already committed to this commitment.")
  else:
    # User can commit to this commitment.
    member = CommitmentMember(user=user, commitment=commitment)
    member.save()
    user.message_set.create(message="You are now committed to \"%s\"" % commitment.title)
  
    # Check for Facebook.
    try:
      import makahiki_facebook.facebook as facebook
      
      fb_user = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_APP_ID, settings.FACEBOOK_SECRET_KEY)
      if fb_user:
        try:
          graph = facebook.GraphAPI(fb_user["access_token"])
          graph.put_object("me", "feed", message="I am now committed to \"%s\" in the Kukui Cup!" % commitment.title)
        except facebook.GraphAPIError:
          # Incorrect user token.
          pass
          
    except ImportError:
      # Facebook not enabled.
      pass
      
  # Redirect back to the referrer or go to the profile if not available.
  ## next = request.META.get("HTTP_REFERER", reverse("makahiki_profiles.views.profile", args=(request.user.id,)))
  next = reverse("pages.view_activities.views.category", args=(commitment.category_id,))
  return HttpResponseRedirect(next)

def __add_activity(request, activity_id):
  """Commit the current user to the activity."""

  activity = get_object_or_404(Activity, pk=activity_id)
  user = request.user

  # Search for an existing activity for this user
  if activity not in user.activity_set.all():
    activity_member = ActivityMember(user=user, activity=activity)
    activity_member.save()
    user.message_set.create(message="You are now participating in the activity \"" + activity.title + "\"")
  else:
    return Http404

  # Redirect back to the referrer or go to the profile if not available.
  next = reverse("pages.view_activities.views.category", args=(activity.category_id,))
  return HttpResponseRedirect(next)
    
def __request_activity_points(request, activity_id):
  """Creates a request for points for an activity."""
  
  activity = get_object_or_404(Activity, pk=activity_id)
  user = request.user
  question = None
  activity_member = None
  
  try:
    # Retrieve an existing activity member object if it exists.
    activity_member = ActivityMember.objects.get(user=user, activity=activity)
    if activity_member.award_date:
      user.message_set.create(message="You have already received the points for this activity.")
      return HttpResponseRedirect(reverse("makahiki_profiles.views.profile", args=(request.user.id,)))
      
  except ObjectDoesNotExist:
    pass # Ignore for now.

  if request.method == "POST":
    if activity.confirm_type == "image":
      form = ActivityImageForm(request.POST, request.FILES)
    elif activity.confirm_type == "free":
      form = ActivityFreeResponseForm(request.POST)
    else:
      form = ActivityTextForm(request.POST)
      
    if form.is_valid():
      if not activity_member:
        activity_member = ActivityMember(user=user, activity=activity)
      
      activity_member.user_comment = form.cleaned_data["comment"]
      # Attach image if it is an image form.
      if form.cleaned_data.has_key("image_response"):
        path = activity_image_file_path(user=user, filename=request.FILES['image_response'].name)
        activity_member.image = path
        new_file = activity_member.image.storage.save(path, request.FILES["image_response"])
        activity_member.approval_status = "pending"
        user.message_set.create(message="Your request has been submitted!")

      elif activity.confirm_type == "code":
        # Approve the activity (confirmation code is validated in forms.ActivityTextForm.clean())
        code = ConfirmationCode.objects.get(code=form.cleaned_data["response"])
        code.is_active = False
        code.save()
        activity_member.approval_status = "approved" # Model save method will award the points.
        points = activity_member.activity.point_value
        message = "You have been awarded %d points for your participation!" % points
        user.message_set.create(message=message)
        
      # Attach text prompt question if one is provided
      elif form.cleaned_data.has_key("question"):
        activity_member.question = TextPromptQuestion.objects.get(pk=form.cleaned_data["question"])
        activity_member.response = form.cleaned_data["response"]
        activity_member.approval_status = "pending"
        user.message_set.create(message="Your request has been submitted!")
                
      elif activity.confirm_type == "free":
        activity_member.response = form.cleaned_data["response"]
        activity_member.approval_status = "pending"
        user.message_set.create(message="Your request has been submitted!")

      activity_member.save()
      next = reverse("pages.view_activities.views.category", args=(activity.category_id,))
      return HttpResponseRedirect(next)
  
    question = activity.pick_question()
                      		  
    return render_to_response("view_activities/task.html", {
    "task":activity,
    "type":"Activity",
    "pau":False,
    "form":form,
    "question":question,
    "member_all":10,
    "member_floor":1,
    }, context_instance=RequestContext(request))    

  
def category(request, category_id):
  TASKS_COL_COUNT = 4
  user = request.user
    
  tasks_list = []
  task_col_list = []
  col_count = 0
  
  title = Category.objects.get(pk=category_id).name
  activities = Activity.objects.filter(category__id=category_id)
  for t in activities:
    pau = ActivityMember.objects.filter(user=user, activity=t).count() > 0
    t.type="Activity"
    task_col_list.append([t, pau])
    col_count = col_count + 1
    if col_count == TASKS_COL_COUNT: 
      tasks_list.append(task_col_list)
      task_col_list = []
      col_count = 0
  
  commitments = Commitment.objects.filter(category__id=category_id)
  for t in commitments:
    pau = CommitmentMember.objects.filter(user=user, commitment=t).count() > 0
    t.type="Commitment"
    task_col_list.append([t, pau])
    col_count = col_count + 1
    if col_count == TASKS_COL_COUNT: 
      tasks_list.append(task_col_list)
      task_col_list = []
      col_count = 0
  		
  tasks_list.append(task_col_list)  
  		  
  return render_to_response("view_activities/category.html", {
    "title":title,
    "tasks":tasks_list,
  }, context_instance=RequestContext(request))
    
def task(request, type, task_id):
  user = request.user
  question = None
  form = None
  
  if type == "Activity":
    task = Activity.objects.get(id=task_id)
    pau = ActivityMember.objects.filter(user=user, activity=task).count() > 0
    
    # Create activity request form.
    if task.confirm_type == "image":
      form = ActivityImageForm()
    elif task.confirm_type == "text":
      question = task.pick_question()
      form = ActivityTextForm(initial={"question" : question.pk})
    elif task.confirm_type == "free":
      form = ActivityFreeResponseForm()
    else:
      form = ActivityTextForm(initial={"code" : 1})
                
    if task.is_event == 1:
      type="Event"   
      
  else:  ## "Commitment"
    task = Commitment.objects.get(id=task_id)
    pau = CommitmentMember.objects.filter(user=user, commitment=task).count() > 0
  		  
  return render_to_response("view_activities/task.html", {
    "task":task,
    "type":type,
    "pau":pau,
    "form":form,
    "question":question,
    "member_all":10,
    "member_floor":1,
  }, context_instance=RequestContext(request))    
    
def add_task(request, type, task_id):
  
  if type == "Activity":
    return __request_activity_points(request, task_id)
  else:
    return __add_commitment(request, task_id)
  
