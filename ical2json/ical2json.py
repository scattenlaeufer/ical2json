#!/usr/bin/env python3

"""
A python script to parse Nextcloud ical calendars to JSON
"""

import argparse
import datetime
import json
import logging
import os
from typing import Dict, List, Optional
import requests
import ical
from ical.calendar import Calendar as IcalCalendar
from ical.calendar_stream import IcsCalendarStream
from pydantic import BaseModel
from rich.logging import RichHandler
from rich.traceback import install

install()

FORMAT = "%(message)s"
LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(
    level=LOGLEVEL, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger(__name__)


class Event(BaseModel):
    """
    Representation of an event for calendar
    """
    uid: str
    summary: str
    start: datetime.datetime | datetime.date
    end: datetime.datetime | datetime.date | None

    @classmethod
    def from_ical_event(cls, event: ical.event.Event):
        """
        Create an Event object from an `ics.event.Event` object

        :param event: Event from which to create the object
        """
        return cls(
            uid=event.uid,
            summary=event.summary,
            start=event.start,
            end=event.end,
        )


class Calendar(BaseModel):
    """
    Representation of a Calendar with an Event list
    """
    name: str
    color: str
    events: list[Event]

    @classmethod
    def from_ics(cls, ics: str):
        """
        Create a Calendar object from an `ics.calendar.Calendar` object

        :param ics: Calendar string in ics format
        """
        ics_calendar = IcsCalendarStream.calendar_from_ics(ics)
        event_list: list[Event] = []
        for event in ics_calendar.timeline:
            event_list.append(Event.from_ical_event(event))
        extras = {e.name: e.value for e in ics_calendar.extras}
        return cls(
            name=extras.get("x-wr-calname", ""),
            color=extras.get("x-apple-calendar-color", "#000000"),
            events=event_list,
        )


def get_ics_calendar(base_url: str, uri: str, user: str, password: str) -> str:
    """
    Pull a ical calendar in ics format from Nextcloud

    :param base_url: The URL of the Nextcloud from where to pull the calendar
    :param uri: The URI of the calendar to pull
    :param user: The user, through which the callendar get's pulled
    :param password: Password for the user
    :return: The calendar in ics format
    """
    log.debug("getting the ical calenadar from nextcloud")

    response = requests.get(
        f"{base_url}/remote.php/dav/calendars/{user}/{uri}",
        auth=(user, password),
        timeout=10,
        params=b"export&accept=ical",
    )

    return response.text


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
    calendar = Calendar.from_ics(ics)
    log.debug(calendar)
    return calendar.json()


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
