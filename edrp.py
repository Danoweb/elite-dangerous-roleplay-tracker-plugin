#! /usr/bin/env python
"""
Methods for generating HTTP requests for the EDRP API.
"""

from __future__ import division, print_function

import json
import requests
from datetime import datetime, timedelta

__version__ = '0.0.3'


class EDRP(object):

    def __init__(self):
        """
        Container for methods used to generate HTTP requests for the EDRP API.
        """
        # URL for the EDRP API.
        self.url = 'https://edrp-api.danowebstudios.com'
        self.logged_in = False
        self.ping_rate_limit = timedelta(minutes=5)
        self.last_message_sent = None

    # Low Level API Functions
    def _post(self, payload):
        """
        Create an HTTP POST request for the EDRP API.
        :param payload: Payload for the HTTP POST request.
        :return: Response from HTTP POST request.
        """
        # Replace spaces in the payload with '+'.
        payload = payload.replace(' ', '+')
        # Make the POST request.
        r = requests.post('{}{}'.format(self.url, payload))
        if r.status_code != 200:
            return None
        self.last_message_sent = datetime.utcnow()
        return r.text

    def _get(self, payload):
        """
        Create an HTTP GET request for the EDRP API.
        :param payload: Payload for the HTTP GET request.
        :return: JSON object received from the EDRP API.
        """
        # Replace spaces in the payload with '+'.
        payload = payload.replace(' ', '+')
        # Make the GET request.
        r = requests.get('{}{}'.format(self.url, payload))
        if r.status_code != 200:
            return None
        return r.json()

    # High Level API Functions
    def post_logon(self, cmdr):
        """
        Set an event marker for a CMDR logging onto the plugin.
        :param cmdr: CMDR name.
        :return:
        """
        self._post('/logon/{}'.format(cmdr))

    def post_logoff(self, cmdr):
        """
        Set an event marker for a CMDR logging off the plugin.
        :param cmder: CMDR name.
        :return:
        """
        self._post('/logoff/{}'.format(cmdr))

    def post_station(self, cmdr, station):
        """
        Set an event marker for a CMDR entering a station.
        :param cmdr: CMDR name.
        :param station: Station name.
        :return:
        """
        self._post('/station/{}/{}'.format(station, cmdr))

    def post_system(self, cmdr, system):
        """
        Set an event marker for a CMDR entering a star system.
        :param cmdr: CMDR name.
        :param system: System name.
        :return:
        """
        self._post('/system/{}/{}'.format(system, cmdr))

    def post_ping(self, cmdr):
        """
        Ping the API if a notification is received from EDMC and it is not too
        soon to send a message according to the last POST request sent and the
        ping rate limit.
        :param cmdr: CMDR name.
        :return bool: Was ping sent?
        """
        if not self.last_message_sent or datetime.utcnow() - self.last_message_sent >= self.ping_rate_limit:
            self._post('/ping/{}'.format(cmdr))
            return True
        return False

    def get_active(self):
        """
        Get a list of users with an event from the plugin within the last 10
        minutes.
        :return: List of user names.
        """
        response_json = self._get('/active')
        if not response_json or 'message' not in response_json:
            return None
        # Message will be returned as a string of JSON that needs to be loaded.
        try:
            msg_json = json.loads(response_json['message'])
        except json.JSONDecodeError:
            err_msg = (
                'Error: Unable to load the JSON response to get_active(): {}'
            ).format(response_json['message'])
            print(err_msg)
            return None
        # Loading the message JSON should give you a list of dictionary objects.
        if type(msg_json) != list:
            return None
        # Pull the CMDR names from the list of dictionaries.
        cmdr_names = []
        for msg_dict in msg_json:
            if 'cmdrName' not in msg_dict:
                print('Unexpected Value: {}'.format(msg_dict))
                continue
            cmdr_names.append(msg_dict['cmdrName'])
        return cmdr_names

    def get_active_count(self):
        """
        Get a count of the users with an event from the plugin within the last 10
        minutes.
        :return: User count.
        """
        response_json = self._get('/active-count')
        if not response_json or 'message' not in response_json:
            return None
        # Message should be a string of an integer value.
        try:
            active_count = int(response_json['message'])
        except ValueError:
            print('Error: Unable to convert the message to an integer: {}'.format(
                    response_json['message']
            ))
            return None
        return active_count
