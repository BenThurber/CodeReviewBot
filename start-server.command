#! /bin/bash

cd "`dirname \"$0\"`"

# Kill python process
pkill -f code-review-picker.py

# If a python virtual environment is not setup, create one
if [ ! -d "./venv-flask/" ]; then
	virtualenv --python=python3 venv-flask
	source venv-flask/bin/activate
	pip install flask
else
	source venv-flask/bin/activate
fi

# Start
echo "Starting code-review-picker.py.  See server.log for output."
rm server.log
nohup python3 code-review-picker.py >>server.log 2>&1 &
