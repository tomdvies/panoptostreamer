import os

import requests
import panoptoauth
import m3u8fetch
# import concurrent
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from render import cache_stream

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
print("\n".join([f"{f['Name']} {f['Id']}" for f in folders]))
# exit()
# print("\n".join([f"{f['Name']} {f['Id']}" for f in folders]))
want = ["II Dynamical Systems MT22", "II Classical Dynamics MT22", "II Galois Theory MT22", "II Representation Theory MT22", "II Asymptotic Methods MT22", "II Applications of Quantum Mechanics LT23", "II Principles of Quantum Mechanics MT22","II Mathematics of Machine Learning LT23","II General Relativity LT23", "II Quantum Information and Computation LT23"]
# want = ["II Linear Analysis MT22", "II Numerical Analysis MT22"]
# folders = [fl for fl in folders if "II" in (fl["Name"] or "III" in fl["Name"] )and fl["Name"] not in remove]# and fl["Name"] in want]
folders = [fl for fl in folders if "II" in (fl["Name"] or "III" in fl["Name"] ) and fl["Name"] in want]
print("\n".join([f"{f['Name']} {f['Id']}" for f in folders]))
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
    session = panoptoauth.get_panopto_token()
    for video in folderreq["d"]["Results"]:
        try:
            link = video["ViewerUrl"]
            name = f"{course['Name'].replace(' ', '_')}/{course['Name'].replace(' ', '_')}_{i}"
            if not os.path.exists(f"cache/{course['Name'].replace(' ', '_')}"):
                os.makedirs(f"cache/{course['Name'].replace(' ', '_')}")
            cache_stream(link, name, session=session)
            i+=1
        except Exception as e:
            print(e)
            with open("log.txt","a") as file:
                file.write(str(e)+"\n")
