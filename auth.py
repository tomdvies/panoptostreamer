import requests
from datetime import datetime
import time

# TODO generate panopto from raven

def getRavenToken(user, passwd):
    print("Fetching panopto tokens...")
    session = requests.Session()
    link = "https://cambridgelectures.cloud.panopto.eu/Panopto/" +\
           "Pages/Auth/Login.aspx?ReturnUrl=https%3A%2F%2Fcambridg" +\
           "electures.cloud.panopto.eu%2FPanopto%2FPages%2FHome.aspx&" +\
           "instance=CambridgeUniversityUISMoodleLIVE&AllowBounce=true"
    re1 = session.get(link)
    session.cookies.set("Ucam-WebAuth-Session-S", "Not-authenticated", domain="www.vle.cam.ac.uk/")
    date = datetime.today().strftime('%Y%m%d%T%H%M%SZ')
    content={
        "date":date,#"20220505T153159Z",
        "iact":"yes",
        "msg":"your session on the site has expired",
        "pwd":passwd,
        "reauth":"1",
        "submit":"Login",
        "url":"https://www.vle.cam.ac.uk/auth/raven/login.php",
        "userid":user,
        "ver":"3"
    }
    # # QWRV5CSCWF
    re2 = session.post("https://raven.cam.ac.uk/auth/authenticate2.html",data=content,cookies={"Ucam-WebAuth-Session-S":"Not-authenticated"})
    "Ucam-WebAuth-Session-S"
    session.cookies.update(re2.history[1].cookies)
    # print(session.cookies)
    re3 = session.get("https://www.vle.cam.ac.uk/auth/raven/login.php")
    for cookie in session.cookies:
        if cookie.name==".ASPXAUTH":
            print("ASPX:",cookie.value)
        if cookie.name=="csrfToken":
            print("csrf:",cookie.value)
    # print(session.cookies)
    return session
# getRavenToken("Qiy5som!DooGidl5","td471")