import requests
from http.cookiejar import MozillaCookieJar

def get_panopto_token():
    print("Fetching panopto tokens...")
    session = requests.Session()
    cj = MozillaCookieJar("mscookies.txt")
    cj.load(ignore_discard=True, ignore_expires=True)
    session.cookies.update(cj)
    # session.headers.update({"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"})
    # session.proxies = {"http":"http://localhost:1234","https":"http://localhost:1234"}
    # session.verify = "/Users/idkwhotomis/.mitmproxy/mitmproxy-ca-cert.pem"
    l1 = "https://cambridgelectures.cloud.panopto.eu/Panopto/Pages/Auth/Login.aspx?Auth=FolderView&ReturnUrl=https%3a%2f%2fcambridgelectures.cloud.panopto.eu%2fPanopto%2fPages%2fSessions%2fList.aspx%3ffolderID%3d50aaf61f-7acc-4e80-824e-af3900d9c0da&ErrorKey=Controls_Login_NoFolderAccess&instance=CambridgeUniversityUISMoodleLIVE&AllowBounce=true"
    re1 = session.get(l1)
    session.cookies.set("Ucam-WebAuth-Session-S", "Not-authenticated", domain="www.vle.cam.ac.uk/")
    re2 = session.get("https://www.vle.cam.ac.uk/auth/saml2/login.php")
    re3 = session.post("https://shib.raven.cam.ac.uk/idp/profile/SAML2/Redirect/SSO?execution=e1s1",
                       data={
                           "shib_idp_ls_exception.shib_idp_session_ss":"",
                           "shib_idp_ls_success.shib_idp_session_ss":"true",
                           "shib_idp_ls_value.shib_idp_session_ss":"",
                           "shib_idp_ls_exception.shib_idp_persistent_ss":"",
                           "shib_idp_ls_success.shib_idp_persistent_ss":"true",
                           "shib_idp_ls_value.shib_idp_persistent_ss":"",
                           "shib_idp_ls_supported":"true",
                           "_eventId_proceed":""
                       }
                       )
    sresp = re3.content.decode().split('"SAMLResponse" value="')[1].split('"')[0]
    re4 = session.post("https://shib.raven.cam.ac.uk/idp/profile/Authn/SAML2/POST/SSO", data={"SAMLResponse":sresp,"RelayState":   "e1s2"})
    re5 = session.post("https://shib.raven.cam.ac.uk/idp/profile/SAML2/Redirect/SSO?execution=e1s3",data={"shib_idp_ls_exception.shib_idp_session_ss":"","shib_idp_ls_success.shib_idp_session_ss":"true","_eventId_proceed":""})
    sresp2 = re5.content.decode().split('"SAMLResponse" value="')[1].split('"')[0]
    re6 = session.post("https://www.vle.cam.ac.uk/auth/saml2/sp/saml2-acs.php/www.vle.cam.ac.uk",
                       data={
                           "RelayState":"https://www.vle.cam.ac.uk/auth/saml2/login.php",
                           "SAMLResponse":sresp2
                             })
    for cookie in session.cookies:
        if cookie.name==".ASPXAUTH":
            print("ASPX:",cookie.value)
        if cookie.name=="csrfToken":
            print("csrf:",cookie.value)
    return session

if __name__ == "__main__":
    get_panopto_token()