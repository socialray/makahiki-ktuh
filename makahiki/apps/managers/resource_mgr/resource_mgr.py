"""resource manager module"""
from django.db.models.aggregates import Count
from apps.managers.team_mgr.models import Team
from apps.widgets.energy_goal.models import EnergyGoal
from apps.managers.resource_mgr.models import EnergyUsage, WaterUsage, ResourceSettings, WasteUsage


def init():
    """initialize the resource manager."""

    if ResourceSettings.objects.count() == 0:
        ResourceSettings.objects.create(name="Energy", unit="kWh", winning_order="Ascending")
        ResourceSettings.objects.create(name="Water", unit="Gallon", winning_order="Ascending")
        ResourceSettings.objects.create(name="Waste", unit="Ton", winning_order="Descending")


def resources_info():
    """returns the managed resource's name."""
    init()
    info = ""
    for resource in ResourceSettings.objects.all():
        info += resource.name + " : " + resource.unit + " : " + resource.winning_order + "\n"
    return info


def team_energy_data(date, team):
    """Return the latest energy data of the current date."""
    energy_data = EnergyUsage.objects.filter(team=team, date=date)
    if energy_data:
        return energy_data[0]
    else:
        return None


def team_energy_usage(date, team):
    """Return the latest energy usage of the current date."""
    energy_data = team_energy_data(date, team)
    if energy_data:
        return energy_data.usage
    else:
        return 0


def resource_ranks(name):
    """return the resource ranking for all teams."""
    team_count = Team.objects.count()
    if name == "Energy":
        resource = EnergyUsage
    elif name == "Water":
        resource = WaterUsage
    elif name == "Waste":
        resource = WasteUsage
    else:
        return None

    init()
    resource_settings = ResourceSettings.objects.get(name=name)
    if resource_settings.winning_order == "Ascending":
        ordering = "usage"
    else:
        ordering = "-usage"

    return resource.objects.order_by("-date", ordering)[:team_count]


def energy_ranks():
    """Get the overall energy ranking for all teams, return an ordered query set."""
    return resource_ranks("Energy")


def waste_ranks():
    """Get the overall waste ranking for all teams, return an ordered query set."""
    return resource_ranks("Waste")


def water_ranks():
    """Get the overall water ranking for all teams, return an ordered query set."""
    return resource_ranks("Water")


def energy_team_rank_info(team):
    """Get the overall rank for the team. Return a dict of the rank number and usage."""
    for idx, rank in enumerate(energy_ranks()):
        if rank.team == team:
            return {"rank": idx + 1, "usage": rank.usage}


def energy_goal_ranks():
    """Generate the scoreboard for energy goals."""
    # We could aggregate the energy goals in teams, but there's a bug in Django.
    # See https://code.djangoproject.com/ticket/13461
    return EnergyGoal.objects.filter(
        goal_status="Below the goal"
    ).values(
        "team__name"
    ).annotate(completions=Count("team")).order_by("-completions")
