# List all recipes
default:
    @just --list

# Run a debug call
debug:
    LOGLEVEL=debug poetry run ical2json/ical2json.py --base-url https://nextcloud.bguth.de --uri mllkalender-1_shared_by_bjoern --user homeassistant --password $(pass nextcloud/homeassistant)

# Run a info callx
info:
    LOGLEVEL=info poetry run ical2json/ical2json.py --base-url https://nextcloud.bguth.de --uri mllkalender-1_shared_by_bjoern --user homeassistant --password $(pass nextcloud/homeassistant)

# Run a call and finish in fx
fx:
    LOGLEVEL=warning poetry run ical2json/ical2json.py --base-url https://nextcloud.bguth.de --uri mllkalender-1_shared_by_bjoern --user homeassistant --password $(pass nextcloud/homeassistant) | fx
