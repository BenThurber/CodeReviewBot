#! /bin/bash

cd "`dirname \"$0\"`"

# Kill if its already running
killall ngrok

# Use the appropriate ngrok binary for the system
if [ "$(uname)" == "Darwin" ]; then
	echo "Using Mac Binary"
	NGROK_BIN=./ngrok_mac/ngrok
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
	echo "Using Linux Binary"
	NGROK_BIN=./ngrok_linux/ngrok
else
	trap 'echo "Can not determine your OS.  Must be Darwin (OSX) or Linux"' EXIT
fi


# Start
echo "Starting ngrok on port 5002.  See ngrok.log for output."
rm ngrok.log
nohup $NGROK_BIN http 5002 -log=stdout > ngrok.log &


# Echo URL after log is created and printed to
TIMEOUT=8
TIME=0
while [ ! -f ./ngrok.log -a  -a "$TIME" -lt "$TIMEOUT" ]
do
	sleep 1;
	((TIME++))
done

sleep 2

echo "These are the urls:"
awk '/url=/{print $9}' ngrok.log | grep http
awk '/url=/{print $8}' ngrok.log | grep https

printf "\n\n"


