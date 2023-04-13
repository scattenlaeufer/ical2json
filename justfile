export LOGLEVEL := "WARNING"
export NEXTCLOUD_URL := `pass ical2json/nextcloud/url`
export NEXTCLOUD_USER := `pass ical2json/nextcloud/user`
export NEXTCLOUD_PASSWORD := `pass ical2json/nextcloud/password`

# List all recipes
default:
    @just --list

# Run a debug call
debug $LOGLEVEL="debug":
    poetry run ical2json/ical2json.py --base-url https://nextcloud.bguth.de --uri mllkalender-1_shared_by_bjoern --user homeassistant --password $(pass nextcloud/homeassistant)

# Run a info callx
info $LOGLEVEL="info":
    poetry run ical2json/ical2json.py --base-url https://nextcloud.bguth.de --uri mllkalender-1_shared_by_bjoern --user homeassistant --password $(pass nextcloud/homeassistant)

# Run a call and finish in fx
fx:
    poetry run ical2json/ical2json.py --base-url https://nextcloud.bguth.de --uri mllkalender-1_shared_by_bjoern --user homeassistant --password $(pass nextcloud/homeassistant) | fx

# Serve the API
serve:
    poetry run uvicorn ical2json.api:app --reload
