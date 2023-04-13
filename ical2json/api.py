"""
Web API to convert a ical calendar to JSON
"""

import os
from fastapi import FastAPI
from ical2json import ical2json


URL = os.environ["NEXTCLOUD_URL"]
USER = os.environ["NEXTCLOUD_USER"]
PASSWORD = os.environ["NEXTCLOUD_PASSWORD"]

app = FastAPI()


@app.get("/nextcloud/cal/{uri}")
def get_nextcloud_calendar(uri: str):
    ical_data = ical2json.get_ics_calendar(URL, uri, USER, PASSWORD)
    calendar = ical2json.Calendar.from_ics(ical_data)
    return calendar


@app.get("/nextcloud/cal/{uri}/from_now")
def get_nextcloud_calendar_from_now(uri: str):
    ical_data = ical2json.get_ics_calendar(URL, uri, USER, PASSWORD)
    calendar = ical2json.Calendar.from_ics(ical_data, True)
    return calendar
