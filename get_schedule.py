#!/usr/bin/env python

import datetime
import json
import time
import urllib.request

from bs4 import BeautifulSoup

def get_url(offset=0) -> str:
    now = datetime.datetime.now()
    offset = datetime.timedelta(days=offset)
    now += offset
    spec = f"https://www.kmhd.org/schedule/{now.year}/{now.strftime('%m')}/{now.strftime('%d')}/"
    return spec

class Show:
    @classmethod
    def from_json(cls, j):
        self = cls()
        self.title = j['program']['title']
        starts = j['start_datetime']
        start = datetime.datetime.fromisoformat(starts[:-2] + ":" + starts[-2:])
        self.start = start.astimezone(datetime.datetime.now().astimezone().tzinfo)
        ends = j['end_datetime']
        end = datetime.datetime.fromisoformat(ends[:-2] + ":" + ends[-2:])
        self.end = end.astimezone(datetime.datetime.now().astimezone().tzinfo)
        return self

    def __repr__(self):
        return f"{self.title} [{self.start} - {self.end}]"

def shows_next_n_days(n) -> [Show]:
    shows = []
    for offset in range(n+1): # Get today and tomorrow
        shows.extend(get_schedule(offset))

    # Return shows that start in the next 24h
    window_start = datetime.datetime.now().astimezone()
    window_end = window_start + datetime.timedelta(days=n)
    return [s for s in shows if window_start < s.start < window_end]

def get_schedule(offset):
    url = get_url(offset)
    page = urllib.request.urlopen(url)
    html = BeautifulSoup(page.read(), "html.parser")
    script = html.find_all("script", id="fusion-metadata")
    # Schedule data is in this javascript variable
    content_prefix = 'Fusion.globalContent='
    b = [l for l in script[0].text.split(';') if l.startswith(content_prefix)]
    if len(b) == 0:
        import PushBullet
        import pushbullet_token
        pb = PushBullet(pushbullet_token.PUSHBULLET_API_TOKEN)
        pb.push_note("VCR Fatal: get_schedule: They changed their javascript!!")
        exit(1)
    raw_js = json.loads(b[0][len(content_prefix):])
    return [Show.from_json(s) for s in raw_js]


def get_next_show_within(n, my_shows_file) -> Show:
    my_shows = load_my_shows(my_shows_file)
    for offset in range(n+1):
        for show in get_schedule(offset):
            if show.title in my_shows and show.start > datetime.datetime.now().astimezone():
                return show

    return None # Nothing coming up :(

def load_my_shows(my_shows_file):
    return set([line.strip() for line in open(my_shows_file).readlines()])

if __name__ == "__main__":
    import sys
    import subprocess
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Scrapes schedule info from KMHD's website")
    parser.add_argument("--shows", help="Path to the shows file. One show-name per line, nothing else.")
    parser.add_argument("--get_shows", help="Print the names of all the shows airing in the next 24h. One per line. Handy to make a shows file which you can remove lines from.", action='store_true')
    args = parser.parse_args()

    if args.get_shows:
        for show in shows_next_n_days(7):
            print(show.title)
        exit(0)

    if args.shows is None:
        sys.stderr.write("ERROR: Must provide a file for show selection with the --shows option\n")
        parser.print_help()
        exit(1)

    selected_shows = load_my_shows(args.shows)
    shows = shows_next_n_days(1)
    shows = [s for s in shows if s.title in selected_shows]
    sys.stderr.write(f"Got {len(shows)} shows\n")

    for show in shows:
        start_rec = show.start - datetime.timedelta(minutes=1)
        end_rec = show.end + datetime.timedelta(minutes=1)
        duration = end_rec - start_rec # One hour, starting 1m early and ending 1m late

        # Using `systemd-run`
        timespec = start_rec.strftime("%Y-%m-%d %H:%M")
        unit_name = f"{show.title}__{duration.seconds}"
        print(f"systemd-run --user --on-calendar=\"{timespec}\" --unit vcr_record@`systemd-escape \"{unit_name}\"`.service")
