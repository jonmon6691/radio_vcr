#!/usr/bin/env bash

cd /home/$USER/src/radio_vcr

ARG=`systemd-escape -u $1`

TITLE=`echo ${ARG} | awk -F'__' '{ print $1 };'`
DUR=`echo ${ARG} | awk -F'__' '{ print $2 };'`
DATESTAMP=`date +%Y-%m-%d`
FILENAME="${DATESTAMP}_$TITLE.mp3"

rec -q "$FILENAME" trim 0 $DUR gain 6
REC=$?

echo File recoreded: `pwd`/$FILENAME

.venv/bin/python upload_to_youtube.py "$FILENAME"
YT=$?

.venv/bin/python notify.py "VCR" "r:$REC u:$YT $FILENAME"


