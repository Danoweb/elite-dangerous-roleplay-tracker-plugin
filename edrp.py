#! /usr/bin/env python
"""
Methods for generating HTTP requests for the EDRP API.
"""

from __future__ import division, print_function

import json
import requests

__version__ = '0.0.1'


EDRP_API_URL = 'http://edrp-api.danowebstudios.com'


# Low Level API Functions
def post(payload):
    """
    Create an HTTP POST request for the EDRP API.
    :param payload: Payload for the HTTP POST request.
    :return: Response from HTTP POST request.
    """
    # Replace spaces in the payload with '+'.
    payload = payload.replace(' ', '+')
    # Make the POST request.
    r = requests.post('{}{}'.format(EDRP_API_URL, payload))
    if r.status_code != 200:
        return None
    return r.text

def get(payload):
    """
    Create an HTTP GET request for the EDRP API.
    :param payload: Payload for the HTTP GET request.
    :return: JSON object received from the EDRP API.
    """
    # Replace spaces in the payload with '+'.
    payload = payload.replace(' ', '+')
    # Make the GET request.
    r = requests.get('{}{}'.format(EDRP_API_URL, payload))
    if r.status_code != 200:
        return None
    return r.json()


# High Level API Functions
def post_logon(cmdr):
    """
    Set an event marker for a CMDR logging onto the plugin.
    :param cmdr: CMDR name.
    :return:
    """
    post('/logon/{}'.format(cmdr))


def post_logoff(cmdr):
    """
    Set an event marker for a CMDR logging off the plugin.
    :param cmder: CMDR name.
    :return:
    """
    post('/logoff/{}'.format(cmdr))


def post_station(cmdr, station):
    """
    Set an event marker for a CMDR entering a station.
    :param cmdr: CMDR name.
    :param station: Station name.
    :return:
    """
    post('/station/{}/{}'.format(station, cmdr))


def post_system(cmdr, system):
    """
    Set an event marker for a CMDR entering a star system.
    :param cmdr: CMDR name.
    :param system: System name.
    :return:
    """
    post('/system/{}/{}'.format(system, cmdr))


def get_active():
    """
    Get a list of users with an event from the plugin within the last 10
    minutes.
    :return: List of user names.
    """
    response_json = get('/active')
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


def get_active_count():
    """
    Get a count of the users with an event from the plugin within the last 10
    minutes.
    :return: User count.
    """
    response_json = get('/active-count')
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
