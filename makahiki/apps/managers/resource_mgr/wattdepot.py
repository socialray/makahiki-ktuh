"""Retrieve the data from the wattdepot."""

from xml.etree.ElementTree import ParseError
import datetime
from requests.exceptions import Timeout
from apps.managers.challenge_mgr import challenge_mgr
from xml.etree import ElementTree
from apps.managers.resource_mgr.storage import ResourceStorage


class Wattdepot(ResourceStorage):
    """Define the wattdepot data retrieval functions."""

    def name(self):
        """returns the name of the resource storage."""
        return "Wattdepot"

    def get_latest_resource_data(self, session, team, date):
        """Returns the latest usage of the specified resource for the current date."""
        start_time = date.strftime("%Y-%m-%dT00:00:00")
        end_time = "latest"

        session.params = {'startTime': start_time, 'endTime': end_time}
        return self._get_energy_usage(session, team.name)

    def get_history_resource_data(self, session, team, date, hour):
        """Return the history energy usage of the team for the date and hour."""
        start_time = date.strftime("%Y-%m-%dT00:00:00")
        if hour and hour < 24:
            end_time = date.strftime("%Y-%m-%dT") + "%.2d:00:00" % hour
        else:
            end_time = (date + datetime.timedelta(days=1)).strftime("%Y-%m-%dT00:00:00")

        session.params = {'startTime': start_time, 'endTime': end_time}
        return self._get_energy_usage(session, team.name)

    def _get_energy_usage(self, session, source):
        """Return the energy usage from wattdepot."""
        rest_url = "%s/sources/%s/energy/" % (
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

            return int(round(float(usage)))

        except Timeout:
            print 'Wattdepot data retrieval for team %s error: connection timeout.' % source
        except ParseError as exception:
            print 'Wattdepot data retrieval for team %s ParseError : %s' % (source, exception)

        return 0
