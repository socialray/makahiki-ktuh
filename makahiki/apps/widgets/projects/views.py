"""Provides the view of the widget."""

from apps.widgets.projects.models import Project, Goal, Comment
from apps.widgets.projects.forms import ProjectForm

def supply(request, page_name):
    """ supply view_object content, which is the projects for this game."""
    
    projects = Project.objects.filter(approved=True)
    goals = Goal.objects.all()
    comments = Comment.objects.all()
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            p = Project(title = form.cleaned_data['title'],
                        short_description = form.cleaned_data['short_description'],
                        long_description = form.cleaned_data['long_description'],
                        max_number_of_members = form.cleaned_data['max_number_of_members']
            )
            p.save()
    else:
        form = ProjectForm()

    _ = request
    _ = page_name
    return {
        "projects": projects,    
        "goals": goals,
        "comments": comments,
        "form": form,
        }

