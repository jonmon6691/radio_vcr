from ytmusicapi import YTMusic
import sys

upfile = sys.argv[1]
m = YTMusic("browser.json")
m.upload_song(upfile)
