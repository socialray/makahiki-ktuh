import datetime

from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User
from activities.models import Activity, ActivityMember
from makahiki_profiles.models import Profile, ScoreboardEntry
    
class ScoreboardEntryUnitTests(TestCase):
  fixtures = ["base_data.json", "user_data.json"]
  
  def setUp(self):
    """Set the competition settings to the current date for testing."""
    self.saved_rounds = settings.COMPETITION_ROUNDS
    self.current_round = "Round 1"
    start = datetime.date.today()
    end = start + datetime.timedelta(days=7)
    
    settings.COMPETITION_ROUNDS = {
      "Round 1" : {
        "start": start.strftime("%Y-%m-%d"),
        "end": end.strftime("%Y-%m-%d"),
      },
    }
    
  def testRoundsUpdate(self):
    """Test that the score for the round updates when an activity is approved."""
    user = User.objects.all()[0]
    entry, created = ScoreboardEntry.objects.get_or_create(
                        profile=user.get_profile(), 
                        round_name=self.current_round,
                      )
    round_points = entry.points
    round_submission_date = entry.last_awarded_submission

    activity = Activity.objects.all()[0]
    activity_points = activity.point_value

    activity_member = ActivityMember(user=user, activity=activity)
    activity_member.approval_status = "approved"
    activity_member.save()
    
    # Verify that the points for the round has been updated.
    entry, created = ScoreboardEntry.objects.get_or_create(
                        profile=user.get_profile(), 
                        round_name=self.current_round,
                      )
                    
    self.assertEqual(round_points + activity_points, entry.points)
    self.assertNotEqual(round_submission_date, entry.last_awarded_submission)
    
  def testRoundDoesNotUpdate(self):
    """Test that the score for the round does not update for an activity submitted outside of the round."""
    user = User.objects.all()[0]
    entry, created = ScoreboardEntry.objects.get_or_create(
                        profile=user.get_profile(), 
                        round_name=self.current_round,
                      )
    round_points = entry.points
    round_submission_date = entry.last_awarded_submission

    activity = Activity.objects.all()[0]
    activity_points = activity.point_value

    activity_member = ActivityMember(user=user, activity=activity)
    activity_member.approval_status = "approved"
    activity_member.submission_date = datetime.datetime.today() - datetime.timedelta(days=1)
    activity_member.save()

    # Verify that the points for the round has not been updated.
    entry, created = ScoreboardEntry.objects.get_or_create(
                        profile=user.get_profile(), 
                        round_name=self.current_round,
                      )
                      
    self.assertEqual(round_points, entry.points)
    self.assertEqual(round_submission_date, entry.last_awarded_submission)
    
  def tearDown(self):
    """Restore the saved settings."""
    settings.COMPETITION_ROUNDS = self.saved_rounds
    
class ProfileUnitTests(TestCase):
  fixtures = ["base_data.json", "user_data.json"]
  
  def testAwardRollback(self):
    """Tests that the last_awarded_submission field rolls back to a previous task."""
    user = User.objects.get(username="user")
    activities = Activity.objects.all()[0:2]
    
    # Submit the first activity.  This is what we're going to rollback to.
    activity_member = ActivityMember(user=user, activity=activities[0])
    activity_member.approval_status = "approved"
    activity_member.submission_date = datetime.datetime.today() - datetime.timedelta(days=1)
    activity_member.save()
    
    points = user.get_profile().points
    submit_date = user.get_profile().last_awarded_submission
    
    # Submit second activity.
    activity_member = ActivityMember(user=user, activity=activities[1])
    activity_member.approval_status = "approved"
    activity_member.submission_date = datetime.datetime.today()
    activity_member.save()
    
    activity_member.approval_status = "rejected"
    activity_member.save()
    
    # Verify that we rolled back to the previous activity.
    self.assertEqual(points, user.get_profile().points)
    self.assertTrue(abs(submit_date - user.get_profile().last_awarded_submission) < datetime.timedelta(minutes=1))
    
class ProfilesFunctionalTestCase(TestCase):
  fixtures = ["base_data.json", "user_data.json"]
  
  def setUp(self):
    self.user = User.objects.get(username="user")
    self.client.post('/account/login/', {"username": self.user.username, "password": "changeme", "remember": False})

  def testLoadProfile(self):
    """Test that we can load the profile page and the boxes are correct."""

    response = self.client.get('/profiles/profile/%s/' % self.user.pk)
    
    # Verify standings are correct.
    self.assertEqual(len(response.context["standings_titles"]), len(response.context["floor_standings"]))
    
    activities = self.user.activity_set.filter(activitymember__award_date=None)
    commitments = self.user.commitment_set.filter(commitmentmember__award_date=None)
    goals = self.user.get_profile().floor.goal_set.filter(goalmember__award_date=None)
    
    self.assertEqual(len(activities), len(response.context["user_activities"]))
    for activity in activities:
      self.assertTrue(activity in response.context["user_activities"])
      
    self.assertEqual(len(commitments), len(response.context["user_commitments"]))
    for commitment in commitments:
      self.assertTrue(commitment in response.context["user_commitments"])
      
    self.assertEqual(len(goals), len(response.context["user_goals"]))
    for goal in goals:
      self.assertTrue(goal in response.context["user_goals"])
      
  def testSelectedTab(self):
    """Test that the current round's tab is selected."""
    
    # Set up rounds for test.
    self.saved_rounds = settings.COMPETITION_ROUNDS
    self.current_round = "Round 1"
    start = datetime.date.today()
    end = start + datetime.timedelta(days=7)
    
    settings.COMPETITION_ROUNDS = {
      "Round 1" : {
        "start": start.strftime("%Y-%m-%d"),
        "end": end.strftime("%Y-%m-%d"),
      },
    }
    
    response = self.client.get('/profiles/profile/%s/' % self.user.pk)
    self.assertEqual(0, response.context["selected_tab"])
    
    start = end
    end = end + datetime.timedelta(days=7)
    settings.COMPETITION_ROUNDS = {
      "Round 1" : {
        "start": start.strftime("%Y-%m-%d"),
        "end": end.strftime("%Y-%m-%d"),
      },
    }
    
    response = self.client.get('/profiles/profile/%s/' % self.user.pk)
    self.assertEqual(1, response.context["selected_tab"])
    
    # Restore settings.
    settings.COMPETITION_ROUNDS = self.saved_rounds