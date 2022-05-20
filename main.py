import os

from moviepy.video.VideoClip import ColorClip
from moviepy.video.fx.crop import crop

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
try:
    os.mkdir("output")
except:
    pass

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

def save_stream2(link, user, password,name):
    print("downloading:",link)
    page_id = link.split("id=")[-1]
    session = auth.getRavenToken(user,password)
    infojson = getInfoJson(page_id, session)
    out_str = f"output/{name}.mp4"
    # print(infojson)
    # name = infojson["Delivery"]["SessionGroupLongName"].replace(" ", "_")
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
        shutil.copy2('tmp/out0.mp4', out_str)
    elif len(videos) == 2:
        final_clip = clips_array([[videos[0].resize(0.6),videos[1]]]).resize((1980,1080))
        final_clip.write_videofile(out_str, threads = 8, fps=24)
    else:
        blank = ColorClip((10,10), (0,0,0), duration=videos[0].duration)
        final_clip = clips_array([[videos[0].resize(0.6),blank],
                                  [videos[1], videos[2].resize(videos[1].size)]]).resize((1980,1080)) # hack for grm
                                  # [videos[1], crop(videos[2],x1=60,x2=videos[2].size[0]-60,y1=30,y2=videos[2].size[1]-30).resize(videos[1].size)]]) # hack for messed up grm camera
        final_clip.write_videofile(out_str, threads = 32, fps=24)
    print("written file,",f'output/{name}.mp4')


with open("info.txt","r") as f:
    file2 = f.read()
    user,pwd = file2.split("\n")[0:2]

# print(data["Results"][0]["ViewerUrl"])
# link_arr = ["https://cambridgelectures.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=65b557be-f61b-40eb-8136-ae2900bb8d68"]
link_arr = ["https://cambridgelectures.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=ce31b744-a8c5-48ee-a361-ae6001010cbd",
            "https://cambridgelectures.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=40612c98-0bd2-4d1d-9b70-ae600101152d",
            "https://cambridgelectures.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=917d0114-f86c-44f0-a7c8-ae6001011ea8",
            "https://cambridgelectures.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=6cec1c27-8032-4aa1-abaa-ae6001010e85",
            "https://cambridgelectures.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=3666edf2-5dfc-40d4-a05e-ae600101170a",
            "https://cambridgelectures.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=9122b2aa-6463-4900-b0a2-ae60010120a9",
            "https://cambridgelectures.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=95f94ad8-b3fa-4b98-913b-ae97007ee102",
            "https://cambridgelectures.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=23e5fe10-3099-43b8-8b33-ae600101195a",
            "https://cambridgelectures.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=85936b1f-3180-43b0-bfa6-ae97007fb69d",
            "https://cambridgelectures.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=1a172d91-161a-4cf2-aefb-ae97008079fd"
            ]
for x in range(len(link_arr)):
    save_stream2(link_arr[x],user,pwd, f"VP_Lecture_{x+1}")

