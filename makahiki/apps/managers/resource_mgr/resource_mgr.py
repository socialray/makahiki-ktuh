"""resource manager module"""
import datetime
from xml.etree.ElementTree import ParseError
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Sum
import requests
from requests.exceptions import Timeout
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.team_mgr.models import Team
from apps.managers.resource_mgr.models import EnergyUsage, WaterUsage, ResourceSettings, \
    WasteUsage
from xml.etree import ElementTree


def init():
    """initialize the resource manager."""

    if ResourceSettings.objects.count() == 0:
        ResourceSettings.objects.create(name="energy", unit="kWh", winning_order="Ascending")
        ResourceSettings.objects.create(name="water", unit="Gallon", winning_order="Ascending")
        ResourceSettings.objects.create(name="waste", unit="Ton", winning_order="Descending")


def resources_info():
    """returns the managed resource's name."""
    init()
    info = ""
    for resource in ResourceSettings.objects.all():
        info += resource.name + " : " + resource.unit + " : " + resource.winning_order + "\n"
    return info


def get_resource_settings(name):
    """returns the resource settings for the specified name."""
    init()
    return ResourceSettings.objects.get(name=name)


def team_resource_data(date, team, resource):
    """Return the latest energy data of the current date."""

    usage = _get_resource_usage(resource)
    energy_data = usage.objects.filter(team=team, date=date)
    if energy_data:
        return energy_data[0]
    else:
        return None


def team_resource_usage(date, team, resource):
    """Return the latest energy usage of the current date."""
    energy_data = team_resource_data(date, team, resource)
    if energy_data:
        return energy_data.usage
    else:
        return 0


def update_energy_usage(date):
    """Update the energy usage from wattdepot server."""

    # workaround the issue that wattdepot might not have the latest data yet.
    date = date - datetime.timedelta(minutes=5)

    start_time = date.strftime("%Y-%m-%dT00:00:00")
    end_time = date.strftime("%Y-%m-%dT%H:%M:%S")

    s = requests.session()
    #s.config['verbose'] = sys.stderr
    s.timeout = 2
    s.params = {'startTime': start_time, 'endTime': end_time}

    for team in Team.objects.all():
        rest_url = "%s/wattdepot/sources/%s/energy/" % (
            settings.CHALLENGE.wattdepot_server_url, team.name)

        try:
            response = s.get(url=rest_url)

            #print response.text
            usage = 0
            property_elements = ElementTree.XML(response.text).findall(".//Property")
            for p in property_elements:
                key_value = p.getchildren()
                if key_value and key_value[0].text == "energyConsumed":
                    usage = key_value[1].text

            #print usage
            try:
                latest_usage = EnergyUsage.objects.get(team=team, date=date.date())
            except ObjectDoesNotExist:
                latest_usage = EnergyUsage(team=team, date=date.date())

            latest_usage.time = date.time()
            latest_usage.usage = int(round(float(usage) / 1000))
            latest_usage.save()
            print 'team %s energy usage updated.' % team
        except Timeout:
            print 'team %s energy usage update error with connection timeout.' % team
        except ParseError as exception:
            print 'team %s energy usage update with ParseError : %s' % (team, exception)


def _get_resource_usage(name):
    """return the resourceusage object by name."""
    if name == "energy":
        return EnergyUsage
    elif name == "water":
        return WaterUsage
    elif name == "waste":
        return WasteUsage
    else:
        return None


def resource_ranks(name, round_name):
    """return the resource ranking for all teams."""
    resource_usage = _get_resource_usage(name)

    resource_settings = get_resource_settings(name)
    if resource_settings.winning_order == "Ascending":
        ordering = "total"
    else:
        ordering = "-total"

    round_info = challenge_mgr.get_round_info(round_name)
    if round_name == "Overall":
        start = settings.COMPETITION_START
        end = settings.COMPETITION_END
    else:
        start = round_info["start"]
        end = round_info["end"]

    ranks = resource_usage.objects.filter(
        date__gte=start.date,
        date__lt=end.date).values("team__name").annotate(
            total=Sum("usage")).order_by(ordering)
    return ranks


def energy_team_rank_info(team):
    """Get the overall rank for the team. Return a dict of the rank number and usage."""
    if team:
        for idx, rank in enumerate(resource_ranks("energy", "Overall")):
            if rank["team__name"] == team.name:
                return {"rank": idx + 1, "usage": rank["total"]}
    else:
        return None
