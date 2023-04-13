#!/usr/bin/env python3

"""
A python script to parse Nextcloud ical calendars to JSON
"""

import argparse
import json
import logging
import os
from typing import Dict,List, Optional
import requests
from ical.calendar import Calendar
from ical.calendar_stream import IcsCalendarStream
from rich.logging import RichHandler
from rich.traceback import install

install()

FORMAT = "%(message)s"
LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(
    level=LOGLEVEL, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger(__name__)


def get_ics_calendar(base_url: str, uri: str, user: str, password: str) -> str:
    """
    Pull a ical calendar in ics format from Nextcloud

    :param base_url: The URL of the Nextcloud from where to pull the calendar
    :param uri: The URI of the calendar to pull
    :param user: The user, through which the callendar get's pulled
    :param password: Password for the user
    :return: The calendar in ics format
    """
    log.debug("getting the ical calendar from nextcloud")

    response = requests.get(
        f"{base_url}/remote.php/dav/calendars/{user}/{uri}",
        auth=(user, password),
        timeout=10,
        params=b"export&accept=ical",
    )

    return response.text


def convert_ics_to_calendar(ics: str) -> Calendar:
    """
    Convert a calendar in .ics format to a Calendar object

    :param ics: String of the ics calendar data
    :return: Parsed Calendar object
    """
    calendar = IcsCalendarStream.calendar_from_ics(ics)

    return calendar


def convert_calendar_to_dict(calendar: Calendar) -> dict:
    """
    Convert a Calendar object to a dictionary

    This contains some meta data and the events in form of a timeline.

    :param calendar: The Calendar object to parse
    :return: The parsed calendar data
    """
    calendar_dict: Dict[str, str|List] = {"x-wr-calname": "n/a"}
    for extra in calendar.extras:
        calendar_dict[extra.name] = extra.value
    event_list: List[Dict[str, Optional[str]]] = []
    for event in calendar.timeline:
        log.debug(event)
        event_dict: Dict[str, Optional[str]] = {
            "uid": event.uid,
            "dtstart": event.dtstart.isoformat(),
            "summary": event.summary,
        }
        if end := event.dtend:
            event_dict["dtend"] = end.isoformat()
        else:
            event_dict["dtend"] = None
        event_list.append(event_dict)
    calendar_dict["events"] = event_list
    return calendar_dict


def main(base_url: str, uri: str, user: str, password: str) -> str:
    """
    General function to parse a Nextcloud calendar in for of a script

    :param base_url: URL to a Nextcloud
    :param uri: URI of the calendar in the Nextcloud
    :param user: User from whom to pull the calendar
    :param password: Password for the user
    :return: The calendar data in JSON format
    """
    log.debug(
        "base_url: %s | uri: %s | user: %s | password: %s",
        base_url,
        uri,
        user,
        password,
    )

    ics = get_ics_calendar(base_url, uri, user, password)
    calendar = convert_ics_to_calendar(ics)
    event_list = convert_calendar_to_dict(calendar)

    log.debug(event_list)

    return json.dumps(event_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A script to parse Nextcloud ical calendars to json"
    )
    parser.add_argument(
        "-c", "--uri", type=str, required=True, help="URI of the calendar to parse"
    )
    parser.add_argument(
        "-u",
        "--user",
        type=str,
        required=True,
        help="Nextcloud user from whom to pull the calendar",
    )
    parser.add_argument(
        "-p", "--password", type=str, required=True, help="Password for the user"
    )
    parser.add_argument(
        "-b", "--base-url", type=str, required=True, help="Nextcloud Base URL"
    )
    args = parser.parse_args()
    log.debug(args)

    calendar_json = main(args.base_url, args.uri, args.user, args.password)
    print(calendar_json)
