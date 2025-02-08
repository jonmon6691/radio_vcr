import ytmusicapi
import sys

upfile = sys.argv[1]
m = ytmusicapi.YTMusic("browser.json")
ret = m.upload_song(upfile)

if ret is ytmusicapi.enums.ResponseStatus.SUCCEEDED:
    sys.stderr.write(f"Upload ok: {upfile}\n")
    exit(0)
else:
    sys.stderr.write(f"Error uploading {upfile}: " + str(ret) + "\n")
    exit(1)

