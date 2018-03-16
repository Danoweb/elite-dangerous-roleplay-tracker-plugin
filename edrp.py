#! /usr/bin/env python
"""
Methods for generating HTTP requests for the EDRP API.
"""

from __future__ import division, print_function

import requests


EDRP_API_URL = 'http://edrp-api.danowebstudios.com'


def post(payload):
    """
    Create an HTTP POST request for the EDRP API.
    :param payload: Payload for the HTTP Post request.
    :return:
    """
    r = requests.post('{}{}'.format(EDRP_API_URL, payload))
    print('Payload: {}'.format(payload))
    print('Status Code: {}'.format(r.status_code))
    print('Response: {}'.format(r.text))


def logon(cmdr):
    """
    Send a logon HTTP request to the EDRP API.
    :param cmdr: CMDR name.
    :return:
    """
    post('/logon/{}'.format(cmdr))


def logoff(cmdr):
    """
    Send a logoff HTTP request to the EDRP API.
    :param cmder: CMDR name.
    :return:
    """
    post('/logoff/{}'.format(cmdr))


def station(station, cmdr):
    """
    Send a station HTTP request to the EDRP API.
    :param station: Station name.
    :param cmdr: CMDR name.
    :return:
    """
    post('/station/{}/{}'.format(station, cmdr))


def system(system, cmdr):
    """
    Send a system HTTP request to the EDRP API.
    :param system: System name.
    :param cmdr: CMDR name.
    :return:
    """
    post('/system/{}/{}'.format(system, cmdr))
