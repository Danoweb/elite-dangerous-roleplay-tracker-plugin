#! /usr/bin/env python
"""
EDRP Plugin For Elite Dangerous Market Connector

Handles events from EDMC and passes the information along to the EDRP API.
"""

from __future__ import division, print_function

import plug
from datetime import datetime
from edrp import EDRP

__version__ = '0.0.2'


# Class that contains all of the EDRP API function calls.
edrp = EDRP()

# Log message format.
LOG_FORMAT = 'EDRP|{date}|{log_level}|{log_source}|{log_msg}'


def log_msg(level, source, msg):
    """
    Print a formatted message, which EDMC will write into the
    EDMarketConnector.log file.
    :param level: Level of log message.
    :param source: Source of the log message.
    :param msg: Message to log.
    :return:
    """
    print(LOG_FORMAT.format(
        date=datetime.utcnow(),
        log_level=level,
        log_source=source,
        log_msg=msg
    ))


def plugin_start():
   """
   Load this plugin into EDMC.
   """
   log_msg('INFO', 'EDMarketConnector', 'Tracker Loaded')
   return None


def plugin_stop():
    """
    EDMC is closing.
    """
    log_msg('INFO', 'EDMarketConnector', 'Tracker Closed')


def prefs_cmdr_changed(cmdr, is_beta):
    """
    Notification that the CMDR has been changed while the settings dialog is open.
    Relevant if you want to have different settings for different user accounts.
    :param cmdr: Current CMDR name (or None).
    :param is_beta: Whether the player is in a Beta universe.
    :return:
    """
    # Doesn't apply unless CMDR specific settings become necessary.
    log_msg('INFO', 'PrefsCmdrChanged', 'New CMDR: {}'.format(cmdr))


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
    # Doesn't apply unless CMDR specific settings become necessary.
    log_msg('INFO', 'PrefsChanged', 'Settings dialog has been closed.')


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
    log_source = 'JournalEntry'
    # Check for an event key.
    if 'event' not in entry:
        log_msg('ERROR', log_source, 'No event key in journal entry: {}'.format(entry))
        error = 'No event key in journal entry.'
        return error

    # Logon Events

    # StartUp: Sent if EDMC is started while the game is already running.
    if entry['event'] == 'StartUp':
        # Unable to detect Open/Group/Solo so assume EDRP.
        edrp.logged_in = True
        log_msg(
            'INFO',
            log_source,
            (
                'StartUp|GameMode: Unknown, Group: Unknown, '
                'CMDR: {}, System: {}, Station: {}'
            ).format(cmdr, system, station)
        )
        edrp.post_logon(cmdr)
        edrp.post_system(cmdr, system)
        edrp.post_station(cmdr, station)
        return error
    # LoadGame: Sent when CMDR logs in to a game mode.
    if entry['event'] == 'LoadGame':
        game_mode = entry.get('GameMode', None)
        group = entry.get('Group', None)
        log_msg(
            'INFO',
            log_source,
            (
                'LoadGame|GameMode: {}, Group: {}, '
                'CMDR: {}, System: {}, Station: {}'
            ).format(game_mode, group, cmdr, system, station)
        )
        if game_mode == 'Group' and group.upper() == 'ED RP':
            edrp.logged_in = True
            edrp.post_logon(cmdr)
            edrp.post_system(cmdr, system)
            edrp.post_station(cmdr, station)
        else:
            edrp.logged_in = False
        return error

    # Do not process anything further if not logged in to the ED RP group.
    if not edrp.logged_in:
        return error

    # Logoff Events

    # ShutDown: Sent when the game is quitted while EDMC is running.
    #       NOTE: This event is not sent when EDMC is running on a different
    #       machine so do not rely on this event.
    if entry['event'] == 'ShutDown':
        log_msg(
            'INFO',
            log_source,
            'ShutDown|CMDR: {}'.format(cmdr)
        )
        edrp.post_logoff(cmdr)
        return error

    # Location Events

    # Docked: Docked at a station.
    if entry['event'] == 'Docked':
        log_msg(
            'INFO',
            log_source,
            'Docked|CMDR {} docked at the {} station in the {} system.'.format(cmdr, station, system)
        )
        edrp.post_system(cmdr, system)
        edrp.post_station(cmdr, station)
    # FSDJump: Arrived in a new system.
    elif entry['event'] == 'FSDJump':
        if 'StarPos' in entry:
            log_msg(
                'INFO',
                log_source,
                'FSDJump|CMDR {} arrived in the {} system. ({}, {}, {})'.format(
                    cmdr,
                    system,
                    *tuple(entry['StarPos'])
                )
            )
        else:
            log_msg(
                'INFO',
                log_source,
                'FSDJump|CMDR {} arrived in the {} system.'.format(cmdr, system)
            )
        edrp.post_system(cmdr, system)
    # Liftoff: Liftoff from a planet's surface.
    elif entry['event'] == 'Liftoff':
        log_msg(
            'INFO',
            log_source,
            'Liftoff|CMDR {} departed from a planet in the {} system.'.format(cmdr, system)
        )
        edrp.post_system(cmdr, system)
    # Location
    elif entry['event'] == 'Location':
        log_msg(
            'INFO',
            log_source,
            'Location|CMDR: {}, System: {}, Station: {}'.format(cmdr, system, station)
        )
        edrp.post_system(cmdr, system)
        edrp.post_station(cmdr, station)
    # Touchdown: Touched down on a planet's surface.
    elif entry['event'] == 'Touchdown':
        log_msg(
            'INFO',
            log_source,
            'Touchdown|CMDR {} landed on a planet in the {} system.'.format(cmdr, system)
        )
        edrp.post_system(cmdr, system)
    # Undocked
    elif entry['event'] == 'Undocked':
        if 'StationName' in entry:
            log_msg(
                'INFO',
                log_source,
                'Undocked|CMDR {} departed from the {} station in the {} system.'.format(
                    cmdr, entry['StationName'], system
                )
            )
        else:
            log_msg(
                'INFO',
                log_source,
                'Undocked|CMDR: {}, System: {}, Station: {}'.format(cmdr, system, station)
            )
        edrp.post_system(cmdr, system)
        edrp.post_station(cmdr, station)
    # Other: Send a ping to the API.
    else:
        if edrp.post_ping(cmdr):
            log_msg('INFO', log_source, 'PING|CMDR: {}'.format(cmdr))

    return error


def dashboard_entry(cmdr, is_beta, entry):
    """
    Receive a dashboard status entry.
    :param cmdr: The piloting CMDR name.
    :param is_beta: Whether the player is in a Beta universe.
    :param entry: The status entry as a dictionary.
    :return: Error message.
    """
    if edrp.post_ping(cmdr):
        log_msg('INFO', 'DashboardEntry', 'PING|CMDR: {}'.format(cmdr))
    return None


def cmdr_data(data, is_beta):
    """
    Receive the latest EDMC data for the CMDR from the FD servers.
    :param data:
    :param is_beta: Whether the player is in a Beta universe.
    :return: Error message.
    """
    if 'commander' in data and 'name' in data['commander']:
        cmdr = data['commander']['name']
        if edrp.post_ping(cmdr):
            log_msg('INFO', 'CmdrData', 'PING|CMDR: {}'.format(cmdr))
    return None
