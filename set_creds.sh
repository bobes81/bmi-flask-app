#!/bin/bash

heroku config:set GOOGLE_CREDS="$(cat creds.json | jq -c .)"
