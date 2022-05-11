import os
import auth
import requests
from http.cookiejar import MozillaCookieJar
from pathlib import Path
import re
import ffmpeg
import shutil


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



def save_stream(link, user, password):
    page_id = link.split("id=")[-1]
    session = auth.getRavenToken(user,password)
    infojson = getInfoJson(page_id, session)
    # print(infojson)
    name = infojson["Delivery"]["SessionGroupLongName"].replace(" ", "_")
    mu3links = []
    for streams in infojson["Delivery"]["Streams"]:
        mu3links += [streams["StreamUrl"]]  # first one is person lecturing, second lhs and third rhs
    # print(mu3links)
    n = 0
    in_file = ffmpeg.input(mu3links[0])
    # ffmpeg.run(in_file)
    # print(in_file)
    # TODO: parallelize this
    audiostream = ffmpeg.output(in_file, f'tmp/audio_stream.mp3', map="0:2").global_args("-codec copy").global_args("-y")
    ffmpeg.run(audiostream)
    for streamlink in mu3links[1::]:
        in_file = ffmpeg.input(streamlink)
        # ffmpeg.run(in_file)
        # print(in_file)
        stream = ffmpeg.output(in_file, f'tmp/stream_{n}.mp4',map="0:1").global_args("-codec copy").global_args("-y")
        ffmpeg.run(stream)
        n+=1
    audio = ffmpeg.input('tmp/audio_stream.aac')
    videos = [ffmpeg.input(file) for file in os.listdir("tmp") if file != "audio_stream.mp3"]
    # (
    #     ffmpeg
    #         .filter([main, logo], 'overlay', 10, 10)
    #         .output('out.mp4')
    #         .run()
    # )

with open("info.txt","r") as f:
    user,pwd = (f.read()).split("\n")
link_arr = ["https://cambridgelectures.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=65b557be-f61b-40eb-8136-ae2900bb8d68"]
for x in link_arr:
    save_stream(x,user,pwd)

