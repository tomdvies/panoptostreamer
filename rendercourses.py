import os

import requests

import panoptoauth
import m3u8fetch
# import concurrent
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
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


session = panoptoauth.get_panopto_token()

folderreq = session.get("https://cambridgelectures.cloud.panopto.eu/Panopto/Api/Folders?parentId=null&folderSet=1&includeMyFolder=false&includePersonalFolders=true&page=0&sort=Depth&names%5B0%5D=SessionCount")
folders = folderreq.json()
remove = ["C0_20_II: II Linear Analysis","HPS Part II Paper 4: HPS Part II Paper 4: Philosophy and Scientific Practice", "Part II Incoming Student Course Options: Part II Incoming Student Course Options",
          "Part III: Introduction to Non-Linear Analysis", "part-ii-pb: Part II Project Briefing","Part II Paper 6: Philosophy of space and time","Geographical Tripos Part II",
          "IIA Engineering","IIB Engineering", "IIA: 3B3: 3B3: Switch-mode Electronics", "IIB: 4A15: 4A15: Acoustics","IIB: 4D10: 4D10: Structural Steelwork","IIB: 4G5: 4G5: Molecular Modelling"]

# want "Id" tag
# print("\n".join([f"{f['Name']} {f['Id']}" for f in folders]))
# want = ["II Applications of Quantum Mechanics LT23", "II Principles of Quantum Mechanics MT22","II Mathematics of Machine Learning LT23","II General Relativity LT23", "II Quantum Information and Computation LT23"]
folders = [fl for fl in folders if "II" in (fl["Name"] or "III" in fl["Name"] )and fl["Name"] not in remove]# and fl["Name"] in want]
course = folders[2]
# print("\n".join([f"{f['Name']} {f['Id']}" for f in folders]))
# this is date ordered
for course in folders:
    # session = panoptoauth.get_panopto_token()
    print(f"Course: {course['Name']}")
    i=1
    fjson = {
        "queryParameters": {
            "bookmarked": False,
            "endDate": None,
            "folderID": course["Id"],
            "getFolderData": True,
            "includeArchived": True,
            "includeArchivedStateCount": True,
            "includePlaylists": True,
            "isSharedWithMe": False,
            "isSubscriptionsPage": False,
            "maxResults": 50,
            "page": 0,
            "query": None,
            "sessionListOnlyArchived": False,
            "sortAscending": True,
            "sortColumn": 1,
            "startDate": None
        }
    }
    folderreq = session.post("https://cambridgelectures.cloud.panopto.eu/Panopto/Services/Data.svc/GetSessions",json=fjson).json()
    # video1 = folderreq["d"]["Results"][0]
    print(f"{len(folderreq['d']['Results'])} lectures to fetch")
    for video in folderreq["d"]["Results"]:
        try:
            link = video["ViewerUrl"]
            name = f"{course['Name']} {i}"
            # print("input:", link)
            # print("output:", name + ".mp4")
            page_id = link.split("&")[0].split("id=")[-1]
            # need to have dumped cookies file at ./mscookies.txt (remove #HttpOnly_ from all of them)
            # session = panoptoauth.get_panopto_token()
            infojson = get_info_json(page_id, session)
            # out_str = f"output/{name}.mp4"
            # print(infojson)
            # name = infojson["Delivery"]["SessionGroupLongName"].replace(" ", "_")
            mu3links = []
            for streams in infojson["Delivery"]["Streams"]:
                mu3links += [streams["StreamUrl"]]  # first one is person lecturing, second lhs and third rhs for most lectures
            print(f"{name}: {len(mu3links)} files to download,")
            #print(mu3links)
            if not os.path.exists(f"m3u8links/{course['Name']}/{name}/"):
                os.makedirs(f"m3u8links/{course['Name']}/{name}/")
            # if os.path.exists(f"rawlectures/{course['Name']}/{name}/completed"):
            #     i+=1
            #     continue
            for j in range(len(mu3links)):
                with open(f"m3u8links/{course['Name']}/{name}/out{j}.m3u8", "wb") as f:
                    # print("url:", playlist.segments[0].absolute_uri)
                    r = requests.get(mu3links[j])
                    f.write(r.content)
             with ThreadPoolExecutor(max_workers=4) as pool:
                 results = pool.map(lambda p: m3u8fetch.download_m3u8(*p),zip(mu3links,
                                                                              [f"m3u8links/{course['Name']}/{name}/out{j}m3u8.mp4" for j in range(len(mu3links))]))
            # Path(f"rawlectures/{course['Name']}/{name}/completed").touch()
            # for j in range(len(mu3links)):
            #     # print(f"downloading file {j + 1}...")
            #     m3u8fetch.download_m3u8(mu3links[j], )
            i+=1
        except Exception as e:
            print(e)
            with open("log.txt","a") as file:
                file.write(str(e)+"\n")
