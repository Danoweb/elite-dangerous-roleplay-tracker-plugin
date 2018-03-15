#! /usr/bin/env python
"""
EDRP Plugin For Elite Dangerous Market Connector

Handles events from EDMC and passes the information along to the EDRP API.
"""

from __future__ import division, print_function

import plug
import edrp


def plugin_start():
   """
   Load this plugin into EDMC
   """
   print('I am loaded!')
   return "Test"


def plugin_stop():
    """
    EDMC is closing
    """
    print('Farewell cruel world!')


def prefs_cmdr_changed(cmdr, is_beta):
    """
    Notification that the CMDR has been changed while the settings dialog is open.
    Relevant if you want to have different settings for different user accounts.
    :param cmdr: Current CMDR name (or None).
    :param is_beta: Whether the player is in a Beta universe.
    :return:
    """
    print('\nCMDR Changed while settings dialog open.')


def prefs_changed(cmdr, is_beta):
    """
    Notification that the settings dialog has been closed.
    The prefs frame and any widgets you created in your `get_prefs()` callback
    will be destroyed on return from this function, so take a copy of any
    values that you want to save.
    :param cmdr: Current CMDR name (or None).
    :param is_beta: Whether the player is in a Beta universe.
    :return:
    """
    print('\nSettings dialog closed.')


def journal_entry(cmdr, is_beta, system, station, entry, state):
    """
    Receive a journal entry.
    :param cmdr: The CMDR name, or None if not yet known.
    :param system: The current system, or None if not yet known.
    :param station: The current station, or None if not docked or not yet known.
    :param entry: The journal entry as a dictionary.
    :param state: A dictionary containing info about the CMDR, current ship and cargo.
    :param is_beta: Whether the player is in a Beta universe.
    :return: Error message.
    """
    error = None
    print('\nJournal Entry Received')
    # StartUp: Sent if EDMC is started while the game is already running.
    if entry['event'] == 'StartUp':
        print('StartUp event received.')
    # LoadGame
    if entry['event'] == 'LoadGame':
        print('LoadGame event received.')
    # Rank
    if entry['event'] == 'Rank':
        print('Rank event received.')
    # Location
    if entry['event'] == 'Location':
        print('Location event received.')
    # ShutDown: Sent when the game is quitted while EDMC is running.
    #       NOTE: This event is not sent when EDMC is running on a different
    #       machine so do not rely on this event.
    if entry['event'] == 'ShutDown':
        print('ShutDown event received.')
    # FSDJump: Arrived in a new system.
    if entry['event'] == 'FSDJump':
        if 'StarPos' in entry:
            print('Arrived at {} ({},{},{})\n'.format(entry['StarSystem'], *tuple(entry['StarPos'])))
        else:
            print('Arrived at {}\n'.format(entry['StarSystem']))
    # Dump information to the log file.
    print('CMDR: {}'.format(cmdr))
    print('is_beta: {}'.format(is_beta))
    print('system: {}'.format(system))
    print('station: {}'.format(station))
    print('entry: {}'.format(entry))
    print('state: {}'.format(state))
    return error


def dashboard_entry(cmdr, is_beta, entry):
    """
    Receive a status entry.
    :param cmdr: The piloting CMDR name.
    :param is_beta: Whether the player is in a Beta universe.
    :param entry: The status entry as a dictionary.
    :return: Error message.
    """
    error = None
    print('\nDashboard Entry Received')
    # Dump information to the log file.
    print('CMDR: {}'.format(cmdr))
    print('is_beta: {}'.format(is_beta))
    print('entry: {}'.format(entry))
    return error


def cmdr_data(data, is_beta):
    """
    Receive the latest EDMC data for the CMDR from the FD servers.
    :param data:
    :param is_beta: Whether the player is in a Beta universe.
    :return: Error message.
    """
    error = None
    print('\nCMDR Data Received')
    # Dump information to the log file.
    print('data: {}'.format(data))
    print('is_beta: {}'.format(is_beta))
    return error
