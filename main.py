import os
import auth
import requests
from http.cookiejar import MozillaCookieJar
from pathlib import Path
import re
import ffmpeg
import shutil
import m3u8fetch
from moviepy.editor import VideoFileClip, clips_array, vfx


try:
    shutil.rmtree("./tmp")
except:
    pass
os.mkdir("./tmp") # make sure you don't use this directory :)))


def parseCookieFile(cookiefile): # horrible fn dont use
    cookies = {}
    with open (cookiefile, 'r') as fp:
        for line in fp:
            if not line.startswith("#") and line.strip()!="":
                lineFields = line.strip().split('\t')
                cookies[lineFields[5]] = lineFields[6]
    return cookies

def getInfoJson(id, session):
    content = {
        "deliveryId": id,
        "invocationId": "",
        "isLiveNotes": "false",
        "refreshAuthCookie": "true",
        "isActiveBroadcast": "false",
        "isEditing": "false",
        "isKollectiveAgentInstalled": "false",
        "isEmbed": "false",
        "responseType": "json"
    }
    return session.post("https://cambridgelectures.cloud.panopto.eu/Panopto/Pages/Viewer/DeliveryInfo.aspx",
                  data=content).json()

# def compositvideo(outname):
#     audio = ffmpeg.input('tmp/audio_stream.aac')
#     videos = [ffmpeg.input(file) for file in os.listdir("tmp") if file != "audio_stream.mp3"]
#     if len(videos) == 1:

def save_stream2(link, user, password):
    page_id = link.split("id=")[-1]
    session = auth.getRavenToken(user,password)
    infojson = getInfoJson(page_id, session)
    # print(infojson)
    name = infojson["Delivery"]["SessionGroupLongName"].replace(" ", "_")
    mu3links = []
    for streams in infojson["Delivery"]["Streams"]:
        mu3links += [streams["StreamUrl"]]  # first one is person lecturing, second lhs and third rhs
    print(f"{len(mu3links)} files to download,")
    for i in range(len(mu3links)):
        print(f"downloading file {i+1}...")
        m3u8fetch.download_m3u8(mu3links[i],f"tmp/out{i}.mp4")
    videos = [VideoFileClip(f"tmp/out{i}.mp4") for i in range(len(mu3links))]
    clip_arrs = []
    if len(videos) == 1:
        videos[0].write_videofile(f"{name}.mp4",threads = 8, fps=24)
    if len(videos) == 2:
        final_clip = clips_array([[videos[0],videos[1]]]).resize((1980,1080))
        final_clip.write_videofile(f"{name}.mp4",threads = 8, fps=24)
    else:
        final_clip = clips_array([[videos[0],videos[0]],
                                  [videos[1], videos[2]]])
        final_clip.write_videofile(f"{name}.mp4",threads = 8, fps=24)


# def save_stream(link, user, password):
#     page_id = link.split("id=")[-1]
#     session = auth.getRavenToken(user,password)
#     infojson = getInfoJson(page_id, session)
#     # print(infojson)
#     name = infojson["Delivery"]["SessionGroupLongName"].replace(" ", "_")
#     mu3links = []
#     for streams in infojson["Delivery"]["Streams"]:
#         mu3links += [streams["StreamUrl"]]  # first one is person lecturing, second lhs and third rhs
#     # print(mu3links)
#     n = 0
#     print(mu3links)
#     in_file = ffmpeg.input(mu3links[0])
#     # ffmpeg.run(in_file)
#     # print(in_file)
#     # TODO: parallelize this
#     audiostream = ffmpeg.output(in_file, f'tmp/stream_0.mp4',codec="copy").global_args("-y")
#     ffmpeg.run(audiostream)
#     for streamlink in mu3links[1::]:
#         in_file = ffmpeg.input(streamlink)
#         # ffmpeg.run(in_file)
#         # print(in_file)
#         # stream = ffmpeg.output(in_file, f'tmp/stream_{n}.mp4',codec="copy").global_args("-y")
#         # ffmpeg.run(stream)
#         n+=1
#     videos = [ffmpeg.input(file) for file in os.listdir("tmp")]
#     """ffmpeg
# 	-i 1.avi -i 2.avi -i 3.avi -i 4.avi
# 	-filter_complex "
# 		nullsrc=size=640x480 [base];
# 		[0:v] setpts=PTS-STARTPTS, scale=320x240 [upperleft];
# 		[1:v] setpts=PTS-STARTPTS, scale=320x240 [upperright];
# 		[2:v] setpts=PTS-STARTPTS, scale=320x240 [lowerleft];
# 		[3:v] setpts=PTS-STARTPTS, scale=320x240 [lowerright];
# 		[base][upperleft] overlay=shortest=1 [tmp1];
# 		[tmp1][upperright] overlay=shortest=1:x=320 [tmp2];
# 		[tmp2][lowerleft] overlay=shortest=1:y=240 [tmp3];
# 		[tmp3][lowerright] overlay=shortest=1:x=320:y=240
# 	"
# 	-c:v libx264 output.mkv"""
#     ffmpeg.filter(videos, "nullsrc")
#     # (
#     #     ffmpeg
#     #         .filter([main, logo], 'overlay', 10, 10)
#     #         .output('out.mp4')
#     #         .run()
#     # )

with open("info.txt","r") as f:
    file2 = f.read()
    user,pwd = file2.split("\n")[0:2]
link_arr = ["https://cambridgelectures.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=65b557be-f61b-40eb-8136-ae2900bb8d68"]
for x in link_arr:
    save_stream2(x,user,pwd)

