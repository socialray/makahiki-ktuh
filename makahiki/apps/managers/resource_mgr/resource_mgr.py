"""Provides services for a specific sustainability "resource" such as energy or water."""

import datetime
from xml.etree.ElementTree import ParseError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Sum
import requests
from requests.exceptions import Timeout
from apps.managers.cache_mgr import cache_mgr
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.team_mgr.models import Team
from apps.managers.resource_mgr.models import EnergyUsage, WaterUsage, ResourceSetting, \
    WasteUsage, ResourceBlackoutDate
from xml.etree import ElementTree
from django.template.defaultfilters import slugify


def get_resource_setting(name):
    """Returns the resource settings for the specified name."""
    resource_setting = cache_mgr.get_cache("resource_setting-%s" % name)
    if resource_setting is None:
        if ResourceSetting.objects.count() == 0:
            ResourceSetting.objects.create(name="energy", unit="kWh", winning_order="Ascending")
            ResourceSetting.objects.create(name="water", unit="Gallon", winning_order="Ascending")
            ResourceSetting.objects.create(name="waste", unit="Ton", winning_order="Descending")

        resource_setting = ResourceSetting.objects.get(name=name)
        cache_mgr.set_cache("resource_setting-%s" % name, resource_setting, 2592000)
    return resource_setting


def is_blackout(date):
    """Returns true if the date falls in the Resource Blackout dates."""
    return ResourceBlackoutDate.objects.filter(date=date).exists()


def team_resource_data(date, team, resource):
    """Returns the latest data for the specified resource on the current date."""

    if not is_blackout(date):
        usage = _get_resource_usage(resource)
        energy_data = usage.objects.filter(team=team, date=date)
        if energy_data:
            return energy_data[0]
        else:
            return None
    else:
        return None


def team_resource_usage(date, team, resource):
    """Returns the latest usage of the specified resource for the current date."""
    energy_data = team_resource_data(date, team, resource)
    if energy_data:
        return energy_data.usage
    else:
        return 0


def team_hourly_energy_usage(date, hour, team):
    """Returns the latest usage of the specified resource for the current date and hour."""
    session = requests.session()
    start_time = date.strftime("%Y-%m-%dT00:00:00")
    end_time = date.strftime("%Y-%m-%dT") + "%.2d:00:00" % hour
    session.params = {'startTime': start_time, 'endTime': end_time}
    return get_energy_usage(session, team.name)


def get_energy_usage(session, source):
    """Return the energy usage from wattdepot."""
    rest_url = "%s/wattdepot/sources/%s/energy/" % (
        challenge_mgr.get_challenge().wattdepot_server_url, source)

    # comment out for debug
    #import sys
    #session.config['verbose'] = sys.stderr

    session.timeout = 5

    try:
        response = session.get(url=rest_url)

        #print response.text
        usage = 0
        property_elements = ElementTree.XML(response.text).findall(".//Property")
        for p in property_elements:
            key_value = p.getchildren()
            if key_value and key_value[0].text == "energyConsumed":
                usage = key_value[1].text

        return int(round(float(usage) / 1000))

    except Timeout:
        print 'team %s energy usage update error with connection timeout.' % source
    except ParseError as exception:
        print 'team %s energy usage update with ParseError : %s' % (source, exception)

    return 0


def update_energy_usage():
    """Update the energy usage from WattDepot server."""

    challenge_mgr.init()
    date = datetime.datetime.today()

    # workaround the issue that wattdepot might not have the latest data yet.
    date = date - datetime.timedelta(minutes=5)

    start_time = date.strftime("%Y-%m-%dT00:00:00")
    end_time = date.strftime("%Y-%m-%dT%H:%M:%S")

    s = requests.session()
    s.params = {'startTime': start_time, 'endTime': end_time}

    for team in Team.objects.all():
        usage = get_energy_usage(s, team.name)
        if usage:
            try:
                latest_usage = EnergyUsage.objects.get(team=team, date=date.date())
            except ObjectDoesNotExist:
                latest_usage = EnergyUsage(team=team, date=date.date())

            latest_usage.time = date.time()
            latest_usage.usage = usage
            latest_usage.save()
            print 'team %s energy usage updated at %s.' % (team, date)


def update_fake_water_usage():
    """update fake water usage."""
    challenge_mgr.init()
    date = datetime.datetime.today()
    for team in Team.objects.all():
        count = team.profile_set.count()
        if count:
            # assume the average water usage is 80 gallon per person per day
            average_usage = 80
            actual_usage = average_usage * 0.9
            water = WaterUsage.objects.filter(team=team, date=date.date())
            if water:
                water = water[0]
            else:
                water = WaterUsage(team=team, date=date.date())

            water.time = date.time()
            water.usage = actual_usage * count
            water.save()
            print 'team %s fake water usage updated at %s.' % (team, date)


def _get_resource_usage(name):
    """Returns the resource usage object by name, or None if not found."""
    if name == "energy":
        return EnergyUsage
    elif name == "water":
        return WaterUsage
    elif name == "waste":
        return WasteUsage
    else:
        return None


def resource_ranks(name, round_name=None):
    """Return the ranking of resource use for all teams."""

    cache_key = "%s_ranks-%s" % (name, slugify(round_name))
    ranks = cache_mgr.get_cache(cache_key)
    if ranks is None:
        resource_usage = _get_resource_usage(name)

        resource_setting = get_resource_setting(name)
        if resource_setting.winning_order == "Ascending":
            ordering = "total"
        else:
            ordering = "-total"

        round_info = challenge_mgr.get_round_info(round_name)
        if not round_info:
            return None

        usage_ranks = resource_usage.objects.filter(
            date__lte=round_info["end"].date).values("team__name").annotate(
                total=Sum("usage")).order_by(ordering)

        ranks = []
        for rank in usage_ranks:
            ranks.append(rank)
        cache_mgr.set_cache(cache_key, ranks, 3600)
    return ranks


def resource_team_rank_info(team, resource):
    """Get the overall rank for the team. Return a dict of the rank number and usage."""
    unit = get_resource_setting(resource).unit
    if team:
        ranks = resource_ranks(resource)
        if ranks:
            for idx, rank in enumerate(ranks):
                if rank["team__name"] == team.name:
                    return {"rank": idx + 1, "usage": rank["total"], "unit": unit, }
    else:
        return None


def resource_leader(name, round_name=None):
    """Returns the leader (team name) of the resource use."""
    ranks = resource_ranks(name, round_name)
    if ranks:
        return ranks[0]["team__name"]
    else:
        return None
