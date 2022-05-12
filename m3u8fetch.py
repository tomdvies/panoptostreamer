import m3u8
import requests
import time

url = "https://d2hpwsdp0ihr0w.cloudfront.net:443/sessions/21d09e28-be01-486b-af5d-ae2900bb8d50/65b557be-f61b-40eb-8136-ae2900bb8d68-bc162f5c-3847-4d42-bd06-ae5a00c504e0.hls/master.m3u8?InvocationID=6a7de538-23d2-ec11-82a6-023c18b7dbd3&tid=00000000-0000-0000-0000-000000000000&StreamID=966dca8b-0532-4520-af68-ae5a00b6a69f&ServerName=cambridgelectures.cloud.panopto.eu"

headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}
playlistroot = m3u8.load(uri=url, headers=headers)
urls = [play.absolute_uri for play in playlistroot.playlists]
playlist = m3u8.load(urls[0]+"?InvocationID=6a7de538-23d2-ec11-82a6-023c18b7dbd3&tid=00000000-0000-0000-0000-000000000000&StreamID=966dca8b-0532-4520-af68-ae5a00b6a69f&ServerName=cambridgelectures.cloud.panopto.eu")

with open("result.mp4","w") as f:
    r = requests.get(playlist.segments[0].absolute_uri)
    f.write(r.content)