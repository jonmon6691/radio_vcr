#!/usr/bin/env python

from pushbullet import PushBullet
from datetime import datetime as dt
import sys

import pushbullet_token

title = sys.argv[1].strip()
body = sys.argv[2].strip()

pb = PushBullet(pushbullet_token.PUSHBULLET_API_TOKEN)
pb.push_note(title, body)
