#! /bin/bash

cd "`dirname \"$0\"`"

export SLACK_VERIFICATION_TOKEN=xbmj1O***REMOVED***
export SLACK_TEAM_ID=***REMOVED***
export FLASK_APP=hello-there.py

python ./hello-there.py