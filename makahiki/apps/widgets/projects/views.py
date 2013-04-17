"""Provides the view of the widget."""
import datetime

from apps.widgets.projects.models import Project, Goal, Comment


def supply(request, page_name):
    """ supply view_object content, which is the projects for this game."""
    projects = Project.objects.all()
    goals = Goal.objects.all()
    comments = Comment.objects.all()
    _ = request
    _ = page_name
    return {
        "projects": projects,    
        "goals": goals,
        "comments": comments,
        }

