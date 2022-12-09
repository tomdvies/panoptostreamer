import requests

# this code is awful, but does generate the desired tokens

def get_raven_token(user, passwd):
    print("Fetching panopto tokens...")
    session = requests.Session()
    link = "https://cambridgelectures.cloud.panopto.eu/Panopto/" +\
           "Pages/Auth/Login.aspx?ReturnUrl=https%3A%2F%2Fcambridg" +\
           "electures.cloud.panopto.eu%2FPanopto%2FPages%2FHome.aspx&" +\
           "instance=CambridgeUniversityUISMoodleLIVE&AllowBounce=true"
    re1 = session.get(link)
    session.cookies.set("Ucam-WebAuth-Session-S", "Not-authenticated", domain="www.vle.cam.ac.uk/")
    content={
        "date":"date",
        "iact":"yes",
        "msg":"your session on the site has expired",
        "pwd":passwd,
        "reauth":"1",
        "submit":"Login",
        "url":"https://www.vle.cam.ac.uk/auth/raven/login.php",
        "userid":user,
        "ver":"3"
    }
    re2 = session.post("https://raven.cam.ac.uk/auth/authenticate2.html",data=content,cookies={"Ucam-WebAuth-Session-S":"Not-authenticated"})
    # this step below seems like it should do nothing as the session should already have the cookies but removing it breaks everything
    session.cookies.update(re2.history[1].cookies)
    re3 = session.get("https://www.vle.cam.ac.uk/auth/raven/login.php")
    for cookie in session.cookies:
        if cookie.name==".ASPXAUTH":
            print("ASPX:",cookie.value)
        if cookie.name=="csrfToken":
            print("csrf:",cookie.value)
    return session

if __name__ == "__main__":
    with open("info.txt","r") as f:
        file2 = f.read()
        user,pwd = file2.split("\n")[0:2]
    get_raven_token(user,pwd)