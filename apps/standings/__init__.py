from django.conf import settings
from django.contrib.auth.models import User
from makahiki_profiles.models import Profile, ScoreboardEntry
import simplejson as json

class StandingsException(Exception):
  def __init__(self, value):
    self.value = value
    
  def __str__(self):
    return repr(self.value)
    
def get_floor_standings_for_user(user):
  """Uses get_standings_for_user to generate standings for each round and the overall 
  standings for users in the user's floor."""
    
  standings = []
  for round_name in settings.COMPETITION_ROUNDS.keys():
    standings.append(get_standings_for_user(user, group="floor", round_name=round_name))
  
  # Append overall standings.
  standings.append(get_standings_for_user(user, group="floor"))
  
  return standings
  
def get_all_standings_for_user(user):
  """Uses get_standings_for_user to generate standings for each round and the overall 
  standings for all users."""

  standings = []
  for round_name in settings.COMPETITION_ROUNDS.keys():
    standings.append(get_standings_for_user(user, group="floor", round_name=round_name))

  # Append overall standings.
  standings.append(get_standings_for_user(user, group="floor"))

  return standings
  
def get_standings_for_user(user, group="floor", round_name=None):
  """Generates standings for a user to be used in the standings widget.  
  Generates either floor-wide standings or standings based on all users.
  Returns a json structure for insertion into the javascript code."""
  
  standings_type = "individual"
  
  # Check for valid standings parameter.
  if group != "floor" and group != "all":
    raise StandingsException("Unknown standings type %s" % standings_type)
    
  user_profile = Profile.objects.get(user=user)
  
  if not user_profile.floor:
    # Nothing we can do again.
    raise StandingsException("User has no floor for standings.")
  
  title = user_entry = entries = None
  if not round_name:
    # Calculate overall standings.
    user_entry = user_profile

    if group == "floor":
      entries = Profile.objects.filter(floor=user_profile.floor).order_by("-points", "-last_awarded_submission")
      title = "Individual standings, %s" % user_profile.floor

    else:
      entries = Profile.objects.all().order_by("-points", "-last_awarded_submission")
      title = "Individual standings, Everyone"
    
  else:
    # Calculate standings for round.
    user_entry = user_profile.scoreboardentry_set.get(round_name=round_name)
    
    if not settings.COMPETITION_ROUNDS or not settings.COMPETITION_ROUNDS.has_key(round_name):
      # Nothing we can do again.
      raise StandingsException("Unknown round name %s" % round_name)
    
    if group == "floor":
      entries = ScoreboardEntry.objects.filter(
                  profile__floor=user_profile.floor,
                  round_name=round_name,
                ).order_by("-points", "-last_awarded_submission")
      title = "Individual standings, %s, %s" % (user_profile.floor, round_name)
    else:
      entries = ScoreboardEntry.objects.filter(round_name=round_name).order_by("-points", "-last_awarded_submission")
      title = "Individual standings, Everyone, %s" % round_name
  
  info, user_index = _calculate_user_standings(user_entry, entries)
  
  # Construct return dictionary.
  return json.dumps({
    "title": title,
    "info": info,
    "myindex": user_index,
    "type": standings_type,
  })
  
def _calculate_user_standings(user_profile, profiles, round=None):
  """Finds user standings based on the user's profile and a list of profiles.
  Returns dictionary of points and the index of the user."""
  
  # First and last users are easy enough to retrieve.
  first = profiles[0]
  profile_count = profiles.count()
  last = profiles[profile_count-1]
  
  # Search for user.
  rank = 1
  above_points = first.points
  below_points = last.points
  found_user = False
  for profile in profiles:
    if profile == user_profile:
      # Set flag that we found the user.
      found_user = True
    elif not found_user:
      # If we haven't found the user yet, keep going.
      above_points = profile.points
      rank += 1
    elif found_user:
      # If we found the user, then this is the person just after.
      below_points = profile.points
      break
      
  # Construct the return dictionary.
  index = 0
  info = [{"points": first.points, "rank": 1, "label": ''}]
  
  # Append above points
  if rank == 2:
    # There's no above points, since that is #1
    index = 1
  elif rank > 2:
    info.append({"points": above_points, "rank": rank - 1, "label": ''})
    index = 2
  
  # Append user points if they are not #1
  if rank > 1:
    info.append({"points": user_profile.points, "rank": rank, "label": ''})

  # Append below and/or last only if the user is not ranked last.
  if rank < profile_count:
    if rank < profile_count - 1:
      # Append the below points if the user is ranked higher than second to last.
      info.append({"points": below_points, "rank": rank + 1, "label": ''})
    info.append({"points": last.points, "rank": profile_count, "label": ''})
    
  return info, index
    
    
      
    
  
  