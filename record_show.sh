#!/usr/bin/env bash

cd /home/$USER/src/radio_vcr

# Parse the commandline arg (unit name after the @ symbol)
ARG=`systemd-escape -u $1`
TITLE=`echo ${ARG} | awk -F'__' '{ print $1 };'`
DUR=`echo ${ARG} | awk -F'__' '{ print $2 };'`
DATESTAMP=`date +%Y-%m-%d`
FILENAME="${DATESTAMP}_$TITLE.mp3"

# Show "on air" screen
/home/$USER/.virtualenvs/pimoroni/bin/python update_screen.py on-air "$TITLE"

# Record the show
rec -q "$FILENAME" trim 0 $DUR gain 6
REC=$?
echo File recoreded: `pwd`/$FILENAME

# Upload it (TODO: This shit breaks like every few days)
.venv/bin/python upload_to_youtube.py "$FILENAME"
YT=$?

# Pushbullet notification, REC and YT are error flags
.venv/bin/python notify.py "VCR" "r:$REC u:$YT $FILENAME"

# Update screen to show the next scheduled recording
/home/$USER/.virtualenvs/pimoroni/bin/python update_screen.py up-next --shows my_shows.ini
