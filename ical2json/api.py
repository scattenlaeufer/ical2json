"""
Web API to convert a ical calendar to JSON
"""

import os
from fastapi import FastAPI
from ical2json import ical2json


app = FastAPI()


@app.get("/nextcloud/cal/{uri}")
def get_nextcloud_calendar(uri: str):
    url = os.environ["NEXTCLOUD_URL"]
    user = os.environ["NEXTCLOUD_USER"]
    password = os.environ["NEXTCLOUD_PASSWORD"]

    ical_data = ical2json.get_ics_calendar(url, uri, user, password)
    calendar = ical2json.Calendar.from_ics(ical_data)
    return calendar
