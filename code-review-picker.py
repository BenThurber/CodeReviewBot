import os

from persistant_sample import PersistantSample
from people import people_id
from flask import abort, Flask, jsonify, request


SLACK_VERIFICATION_TOKEN = "xoxb-948117482785-1293493043892-rBFq9yFiog1f67Pk98u9W0MT"  # Not sure what this is for

SLACK_BOT_TOKEN = "xbmj1O***REMOVED***"
SLACK_TEAM_ID = "***REMOVED***"

PORT = 5002


app = Flask(__name__)


def people_generator():
    """Return a generator of people from a random PersistantSample."""
    rand_index = PersistantSample(len(people_id), "people")
    all_ids = list(people_id.keys())
    while (not rand_index.is_last()):
        user_id = all_ids[rand_index.next()]
        yield user_id, people_id[user_id]


def is_request_valid(request):
    print("Bot Token: " + request.form['token'])
    print("Team Id: " + request.form['team_id'])
    is_token_valid = request.form['token'] == SLACK_BOT_TOKEN
    is_team_id_valid = request.form['team_id'] == SLACK_TEAM_ID

    return is_token_valid and is_team_id_valid


def message():
    while (True):
        name_generator = people_generator()
        new_round_msg = "A new round of code reviews have begun.\n"
        
        for user_id, name in name_generator:
            msg = new_round_msg
            msg += "<@{0}> You have been picked to do a code review by Robbie the Robot.".format(user_id)
            yield msg
            new_round_msg = ""

MSG_GENERATOR = message()



#-----Controller-------

@app.route('/review', methods=['POST'])
def request_code_reviewer():
    if not is_request_valid(request):
        abort(400)

    return jsonify(
        response_type='in_channel',
        text=next(MSG_GENERATOR),
    )




if __name__ == "__main__":
    app.run(port=PORT)






