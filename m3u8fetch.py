import m3u8
import requests
import re
from moviepy.editor import VideoFileClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time

def fetch_clip_to_tmp(url):
    r = requests.get(url, allow_redirects=True)
    filename = url.split("/")[-1]
    open(f"tmp/{filename}", 'wb').write(r.content)  # assumes nothing's name in server has a collision locally
    print(f"fetched {filename}")
    return f"tmp/{filename}"


def download_m3u8(url, outfile):
    playlistroot = m3u8.load(uri=url)
    # print(playlistroot.playlists)
    urls = [play.absolute_uri for play in playlistroot.playlists]
    playlist = m3u8.load(([play.absolute_uri for play in playlistroot.playlists if play.stream_info.resolution[0]==960] + [playlistroot.playlists[0].absolute_uri])[0])
    # print([play.stream_info.resolution[0] for play in playlistroot.playlists])
    # print(([play for play in playlistroot.playlists if play.stream_info.resolution[0]==960] + [playlistroot.playlists[0]])[0].stream_info.resolution[0])
    if not playlist.segments[0].absolute_uri.endswith(".ts"):
        with open(outfile,"wb") as f:
            print("url:",playlist.segments[0].absolute_uri)
            r = requests.get(playlist.segments[0].absolute_uri)
            f.write(r.content)
    else:
        print(f"fetching {len(playlist.segments)} clips")
        # bit hacky has alot of faith in content supplied, also might up render time by crazy amounts
        # should be fine as almost no videos have actual streams of videos
        fclips = []
        processes = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            for clip in playlist.segments:
                processes.append(executor.submit(fetch_clip_to_tmp, clip.absolute_uri))
        for task in as_completed(processes):
            fclips.append(task.result())
        fclips.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
        # for clip in playlist.segments:
        #     fclips.append(f"tmp/{filename}")
        print(f"concatenating {len(playlist.segments)} clips")
        vclips = [VideoFileClip(path) for path in fclips]
        out = concatenate_videoclips(vclips)
        out.write_videofile(outfile, threads = 32, fps=24)


def download_m3u8_local(infile, outfile):
    playlistroot = m3u8.load(uri=url)
    # print(playlistroot.playlists)
    urls = [play.absolute_uri for play in playlistroot.playlists]
    playlist = m3u8.load(([play.absolute_uri for play in playlistroot.playlists if play.stream_info.resolution[0]==960] + [playlistroot.playlists[0].absolute_uri])[0])
    # print([play.stream_info.resolution[0] for play in playlistroot.playlists])
    # print(([play for play in playlistroot.playlists if play.stream_info.resolution[0]==960] + [playlistroot.playlists[0]])[0].stream_info.resolution[0])
    if not playlist.segments[0].absolute_uri.endswith(".ts"):
        with open(outfile,"wb") as f:
            print("url:",playlist.segments[0].absolute_uri)
            r = requests.get(playlist.segments[0].absolute_uri)
            f.write(r.content)
    else:
        print(f"fetching {len(playlist.segments)} clips")
        # bit hacky has alot of faith in content supplied, also might up render time by crazy amounts
        # should be fine as almost no videos have actual streams of videos
        fclips = []
        processes = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            for clip in playlist.segments:
                processes.append(executor.submit(fetch_clip_to_tmp, clip.absolute_uri))
        for task in as_completed(processes):
            fclips.append(task.result())
        fclips.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
        # for clip in playlist.segments:
        #     fclips.append(f"tmp/{filename}")
        print(f"concatenating {len(playlist.segments)} clips")
        vclips = [VideoFileClip(path) for path in fclips]
        out = concatenate_videoclips(vclips)
        out.write_videofile(outfile, threads = 32, fps=24)
