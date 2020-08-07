import os
from slack import RTMClient
from slack.errors import SlackApiError

ACCESS_TOKEN="***REMOVED***"
BOT_USER_ACCESS_TOKEN = "***REMOVED***"

BOT_TOKEN_FROM_SLACK_APPS = "***REMOVED***"


TOKEN = BOT_TOKEN_FROM_SLACK_APPS

#client = WebClient(token=os.environ['SLACK_API_TOKEN'])
#client = WebClient(token=TOKEN)

@RTMClient.run_on(event='message')
def say_hello(**payload):
    print("Got something: " + payload)
    os.system("say hi")
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    if 'text' in data and 'test' in data.get('text', []):
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        try:
            response = web_client.chat_postMessage(
                channel=channel_id,
                text=f"Hi <@{user}>!",
                thread_ts=thread_ts
            )
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")

rtm_client = RTMClient(token=TOKEN)
rtm_client.start()