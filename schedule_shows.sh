#!/usr/bin/env bash

cd /home/$USER/src/radio_vcr

bash <(.venv/bin/python get_schedule.py --shows my_shows.ini)
