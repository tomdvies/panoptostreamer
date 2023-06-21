import os
from moviepy.video.VideoClip import ColorClip
import panoptoauth
import shutil
import m3u8fetch
from moviepy.editor import VideoFileClip, clips_array


try:
    shutil.rmtree("./tmp")
except:
    pass
os.mkdir("./tmp") # make sure you don't use this directory :)))
try:
    os.mkdir("output")
except:
    pass


def get_info_json(id, session):
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

def save_stream(link, user, password, name, session=None): 
    print("input:",link)
    print("output:",name+".mp4")
    page_id = link.split("&")[0].split("id=")[-1]
    # need to have dumped cookies file at ./mscookies.txt
    session = panoptoauth.get_panopto_token()
    infojson = get_info_json(page_id, session)
    out_str = f"output/{name}.mp4"
    # print(infojson)
    # name = infojson["Delivery"]["SessionGroupLongName"].replace(" ", "_")
    mu3links = []
    for streams in infojson["Delivery"]["Streams"]:
        mu3links += [streams["StreamUrl"]]  # first one is person lecturing, second lhs and third rhs for most lectures
    print(f"{len(mu3links)} files to download,")
    for i in range(len(mu3links)):
        print(f"downloading file {i+1}...")
        m3u8fetch.download_m3u8(mu3links[i],f"tmp/out{i}.mp4")
    # moviepy/ffmpeg can be painfully slow, but it does work.
    # a better solution would be much appreciated
    videos = [VideoFileClip(f"tmp/out{i}.mp4") for i in range(len(mu3links))]
    clip_arrs = []
    if len(videos) == 1:
        shutil.copy2('tmp/out0.mp4', out_str)
    else:
        if len(videos) == 2:
            final_clip = clips_array([[videos[0].resize(0.6),videos[1]]])
        else:
            blank = ColorClip((10,10), (0,0,0), duration=videos[0].duration)
            final_clip = clips_array([[videos[0].resize(0.7),blank],
                                      [videos[1], videos[2].resize(width=videos[1].w)]])
                                      # [videos[1], crop(videos[2],x1=60,x2=videos[2].size[0]-60,y1=30,y2=videos[2].size[1]-30).resize(videos[1].size)]]) # hack for messed up grm camera
        # need even dimensions for standard encodings
        if final_clip.w % 2 == 1:
            final_clip = final_clip.margin(right=1)
        if final_clip.h % 2 == 1:
            final_clip = final_clip.margin(top=1)
        final_clip.write_videofile(out_str, threads = 32, fps=24)
                                   # threads=5,
                                   # bitrate="2000k",
                                   # audio_codec="aac",
                                   # codec="h264_videotoolbox")

    print("written file,",out_str)

if __name__ == "__main__":
    with open("info.txt","r") as f:
        file2 = f.read()
        user,pwd = file2.split("\n")[0:2]



