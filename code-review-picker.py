import os

from id_chooser import IdChooser, PersistantIdChooser
from people import ID_TO_NAME
from flask import abort, Flask, jsonify, request
from urllib.parse import urlparse


SLACK_VERIFICATION_TOKEN = "xoxb-948117482785-1293493043892-rBFq9yFiog1f67Pk98u9W0MT"  # Not sure what this is for

SLACK_BOT_TOKEN = "xbmj1O***REMOVED***"
SLACK_TEAM_ID = "***REMOVED***"

#-------Message-Strings-------
MISSING_URL_MSG = "Robby here.  Your missing the URL to your code review, {}."
NEW_ROUND_MESSAGE = "A new round of code reviews have begun."
CODE_REVIEW_MESSAGE = "<@{0}>, Robbie the Robot has picked you to do a code review for {1}."

ID_CHOOSER = PersistantIdChooser(ID_TO_NAME.keys(), "people")

PORT = 5002


app = Flask(__name__)



def code_review_message(sender_id, url):
    message = []
    
    user_id = ID_CHOOSER.next([sender_id])
    message.append(CODE_REVIEW_MESSAGE.format(ID_TO_NAME[user_id], ID_TO_NAME[sender_id]))
    
    message.append(url)
    
    if ID_CHOOSER.is_new_round():
        message.insert(0, NEW_ROUND_MESSAGE)
    
    return "\n".join(message)



#-----Controller-------

@app.route('/review', methods=['POST'])
def request_code_reviewer():
    """Accept a POST request from Slack, triggered by: /review <text>"""
    sender_id = request.form['user_id']
    sender_name = ID_TO_NAME[sender_id]
    
    if not is_request_valid(request):
        abort(403)
    
    # Return no URL entered message
    if not is_valid_URL(request.form['text']):
        return jsonify(
            response_type='ephemeral',  # This part doesn't work.
            text=MISSING_URL_MSG.format(sender_name)
        )
    
    # Return code review message
    return jsonify(
        response_type='in_channel',
        text=code_review_message(sender_id, request.form['text']),
    )


def is_request_valid(request):
    """Check token and team_id"""
    print("Bot Token: " + request.form['token'])
    print("Team Id: " + request.form['team_id'])
    is_token_valid = request.form['token'] == SLACK_BOT_TOKEN
    is_team_id_valid = request.form['team_id'] == SLACK_TEAM_ID

    return is_token_valid and is_team_id_valid


def is_valid_URL(url):
    """Helper function to validate a URL string"""
    
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False    



if __name__ == "__main__":
    app.run(port=PORT)






