import m3u8
import requests

def download_m3u8(url, outfile):
    playlistroot = m3u8.load(uri=url)
    urls = [play.absolute_uri for play in playlistroot.playlists]
    print(urls)
    playlist = m3u8.load(urls[0])
    with open(outfile,"wb") as f:
        r = requests.get(playlist.segments[0].absolute_uri)
        f.write(r.content)