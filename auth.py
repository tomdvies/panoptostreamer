import requests
from datetime import datetime
import time

# TODO generate panopto from raven

def getRavenToken(passwd, user):
    session = requests.Session()
    link = "https://cambridgelectures.cloud.panopto.eu/Panopto/" +\
           "Pages/Auth/Login.aspx?ReturnUrl=https%3A%2F%2Fcambridg" +\
           "electures.cloud.panopto.eu%2FPanopto%2FPages%2FHome.aspx&" +\
           "instance=CambridgeUniversityUISMoodleLIVE&AllowBounce=true"
    re1 = session.get(link)
    session.cookies.set("Ucam-WebAuth-Session-S", "Not-authenticated", domain="www.vle.cam.ac.uk/")
    print(re1.history[1].cookies)

    # req1 = session.get(link).history[1]
    # print(req1.cookies)
    date = datetime.today().strftime('%Y%m%d%T%H%M%SZ')
    # timed = int(time.time())
    # cookies = {
    #     # "_ga_QWRV5CSCWF":"GS1.1.1651866555.1.0.1651866555.0",
    #     "_ga_QWRV5CSCWF":"GS1.1.1651866555.1.0.1651866555.0",
    #     "_ga":"GA1.1.2033646193.1651866556"
    # }
    content={
        "date":date,#"20220505T153159Z",
        "iact":"yes",
        "msg":"your session on the site has expired",
        "pwd":password,
        "reauth":"1",
        "submit":"Login",
        "url":"https://www.vle.cam.ac.uk/auth/raven/login.php",
        "userid":user,
        "ver":"3"
    }
    # # QWRV5CSCWF
    re2 = session.post("https://raven.cam.ac.uk/auth/authenticate2.html",data=content,cookies={"Ucam-WebAuth-Session-S":"Not-authenticated"})
    "Ucam-WebAuth-Session-S"
    print(re2.history[1].cookies)
    session.cookies.update(re2.history[1].cookies)
    print(session.cookies)
    print(session.get("https://www.vle.cam.ac.uk/auth/raven/login.php").cookies)
    print(session.cookies)
    return session
    # print(requests.get(f"https://raven.cam.ac.uk/auth/authenticate.html?ver=3&url=https%3a%2f%2fwww.vle.cam.ac.uk%2fauth%2fraven%2flogin.php&date={date}&iact=yes").content)
    # req2 = session.post("https://raven.cam.ac.uk/auth/authenticate2.html",data=content, allow_redirects=False)
    # next = req2.next.url
    # for cookie in session.cookies:
    #     cookies[cookie.name]=cookie.value
    # print(session.cookies)
    # print(session.get(next, cookies=cookies).content)
    # print(requests.post("https://raven.cam.ac.uk/auth/authenticate2.html",data=content,cookies=cookie2).content)
user = "#"#input("user: ")
password = " "#input("passwd: ")
getRavenToken(password, user)