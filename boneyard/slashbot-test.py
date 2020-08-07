import os
import time
import numpy as np
import re
from slackclient import SlackClient
import datetime


TOKEN = "xbmj1O***REMOVED***"


def post_annotation(token, text=None, channel='bot', response_to=''):
    """
    Post a message into a channel the number of annotated pictures or a other text.
    :param token: Slack API token
    :param text: text to post. If None, the text is the information about the annotations
    :param channel: channel where the bot post the message
    :param reponse_to: if we want to mention some one
    """
    # connection
    slack_client = SlackClient(token)
    # Number of rows and positive samples
    with open("annotation.txt", 'r') as f:
        annotation = f.read().split('\n')[:-1]
    tot = len(annotation), 
    pos =len([p for p in annotation if p.split(', ')[5] == '1'])
    # Mention someone (need an user ID, not an username)
    if response_to != '' :
        response_to = '<@%s>' % response_to
    # Pre-defined message
    if not text:
        text = '%s _%s_\nYou have annotated *%d* pictures \with *%d*     fractures :+1:' % (response_to, np.random.choice(sw_sentences), tot, pos)
    # Post message
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=text)