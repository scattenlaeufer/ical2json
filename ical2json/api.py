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
    calendar = ical2json.convert_ics_to_calendar(ical_data)
    calendar_dict = ical2json.convert_calendar_to_dict(calendar)
    return calendar_dict
