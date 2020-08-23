## Slack Slashbot for assigning Merge Requests

### Background
While working on a Software Engineering group project at Canterbury University, our team needed a way to randomly pick 
team members to do code reviews.  GitLab Merge requests were connected to out Slack workspace.  This bot was written to 
randomly assign Slack members to review a merge request.

Slack users are shuffled into a random pool (a random sample) and picked until none are left.  If any users weren't 
picked from the last round (i.e. you request a code review, but your name is the last one in the pool) they are added 
to the top of the next round.  The state of the code review round is saved persistantly in `obj/` with Python's pickle 
library, so the bot server can be started and stopped without losing the order of code reviews.

### Usage
In Slack a merge request is chosen by typing `/review <URL>`

The bot will return a message that looks like:
![Slack Bot Screenshot](https://raw.githubusercontent.com/BenThurber/CodeReviewBot/master/screenshot.png)


### Setup

#### Requirements
• Python3  
• free ngrok account  
• unix machine to host the bot  

#### Start ngrok
[ngrok](https://ngrok.com/) creates a secure tunnel to your localhost so you don't have to register a domain name for your server.  

cd into the directory containing the ngrok binary for your system `ngrok_mac/` or `ngrok_linux/` and configure your 
authtoken as described on the ngrok website.  On the machine you will use to host the bot, run the script 
`start-ngrok.command` (which will choose the correct ngrok binary for your system).  It will start a background service 
using nohup, and print http and https addresses to access your localhost from (see ngrok.log for errors).

#### Configure Slack slashbot API
Register a new Slack slashbot through https://api.slack.com/apps and install it to your workspace.

Under the features tab on the left, choose "Slash Commands" with the Command as "/review" and the Request URL as the 
HTTP address given by ngrok in the previous step.  

Under the Settings tab, choose "Basic Incformation" and under "App Credentials" copy the Verification Token.  

In the URL of your Slack workspace, copy your team ID as described [here](https://stackoverflow.com/questions/40940327/what-is-the-simplest-way-to-find-a-slack-team-id-and-a-channel-id).

#### Add environment Variables
Add the environment variables `SLACK_BOT_TOKEN` and `SLACK_TEAM_ID` to your system, that you found in the previous step.

#### Add Slack users
The file `people.py` is a python dictionary of Slack User IDs and Screen Names.  Add the IDs of your users.  (User Ids 
can be found on a User's Slack profile).  A user's name doesn't have to match their name in Slack.

#### Start Server
On the same machine you started ngrok, run the script `start-server.command`.