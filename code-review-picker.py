import os

from random import sample 
from people import people_id
from flask import abort, Flask, jsonify, request


def people_generator():
    random_ids = sample(people_id.keys(), len(people_id))
    for random_id in random_ids:
        yield random_id, people_id[random_id]


SLACK_VERIFICATION_TOKEN = "xoxb-948117482785-1293493043892-0imN42LZTgG66jl1r49F8jHH"  # Not sure what this is for

SLACK_BOT_TOKEN = "xbmj1O***REMOVED***"
SLACK_TEAM_ID = "***REMOVED***"

PORT = 5002


app = Flask(__name__)


def is_request_valid(request):
    is_token_valid = request.form['token'] == SLACK_BOT_TOKEN
    is_team_id_valid = request.form['team_id'] == SLACK_TEAM_ID

    return is_token_valid and is_team_id_valid


@app.route('/review', methods=['POST'])
def request_code_reviewer():
    if not is_request_valid(request):
        abort(400)

    return jsonify(
        response_type='in_channel',
        text=next(MSG_GENERATOR),
    )


def message():
    while (True):
        print("A new random round has begun")
        name_generator = people_generator()
        
        for user_id, name in name_generator:
            msg = "<@{0}> You have been picked to do a code review by Robbie the Robot.".format(user_id)
            yield msg

MSG_GENERATOR = message()


if __name__ == "__main__":
    app.run(port=PORT)






