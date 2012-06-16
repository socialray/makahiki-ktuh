"""Prepare rendering of popular smart grid actions widget"""

from apps.widgets.smartgrid import   smartgrid


def supply(request, page_name):
    """Supply view_objects content, which are the popular actions from the smart grid game."""

    _ = request
    num_results = 5 if page_name != "status" else None

    #contruct a dictionary containing the most popular tasks.
    #The keys are the type of the task and the values are a list of tasks."""
    popular_tasks = {
        "Activity": smartgrid.get_popular_actions("activity", "approved", num_results),
        "Commitment": smartgrid.get_popular_actions("commitment", "approved", num_results),
        "Event": smartgrid.get_popular_actions("event", "pending", num_results),
        "Excursion": smartgrid.get_popular_actions("excursion", "pending", num_results),
        }
    count = len(popular_tasks)
    return {
        "popular_tasks": popular_tasks,
        "no_carousel": page_name == "status",
        "range": count,
        }
