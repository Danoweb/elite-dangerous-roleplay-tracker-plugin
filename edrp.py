#! /usr/bin/env python
"""
Methods for generating HTTP requests for the EDRP API.
"""

from __future__ import division, print_function

import requests


EDRP_API_URL = 'http://edrp-api.danowebstudios.com'


# Low Level API Functions
def post(payload):
    """
    Create an HTTP POST request for the EDRP API.
    :param payload: Payload for the HTTP POST request.
    :return:
    """
    r = requests.post('{}{}'.format(EDRP_API_URL, payload))
    print('Payload: {}'.format(payload))
    print('Status Code: {}'.format(r.status_code))
    print('Response: {}'.format(r.text))


def get(payload):
    """
    Create an HTTP GET request for the EDRP API.
    :param payload: Payload for the HTTP GET request.
    :return: JSON object received from the EDRP API.
    """
    r = requests.get('{}{}'.format(EDRP_API_URL, payload))
    print('Payload: {}'.format(payload))
    print('Status Code: {}'.format(r.status_code))
    print('Response: {}'.format(r.text))
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


def post_station(station, cmdr):
    """
    Set an event marker for a CMDR entering a station.
    :param station: Station name.
    :param cmdr: CMDR name.
    :return:
    """
    post('/station/{}/{}'.format(station, cmdr))


def post_system(system, cmdr):
    """
    Set an event marker for a CMDR entering a star system.
    :param system: System name.
    :param cmdr: CMDR name.
    :return:
    """
    post('/system/{}/{}'.format(system, cmdr))


def get_active():
    """
    Get a list of users with an event from the plugin within the last 10
    minutes.
    :return: List of user names.
    """
    # TODO: Once the format for the returned object is discovered, update
    #       this to check for list content and then return the actual list
    #       if it is present.
    active_json = get('/active')
    return active_json


def get_active_count():
    """
    Get a count of the users with an event from the plugin within the last 10
    minutes.
    :return: User count.
    """
    # TODO: Once the format for the returned object is discovered, update
    #       this to check for list content and then return the actual list
    #       if it is present.
    active_count_json = get('/active-count')
    return active_count_json
