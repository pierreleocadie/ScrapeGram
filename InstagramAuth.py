import requests, constants, json, logging
from encrypt_password import encrypt_password
from bs4 import BeautifulSoup

class InstagramAuth:
    
    def __init__(self, username: str, password: str) -> None:
        logging.info("Authenticating...")
        self.session: requests.Session = requests.Session()
        self.username: str = username
        self.password: str = self.enc_password(password)
        self.csrftoken: str = self.get_csrftoken()
        self.mid: str = self.get_mid()
        
        self.session.headers.update({
            "user-agent": constants.USER_AGENT,
            "X-CSRFToken": self.csrftoken,
        })
        logging.debug("Session headers updated")
        self.session.cookies.update({
            "mid": self.mid,
            "csrftoken": self.csrftoken,
        })
        logging.debug("Session cookies updated")
        self.payload: dict = {
            "username": self.username,
            "enc_password": self.password,
        }
        logging.debug("Payload created")
        
        self.login_request = self.login(self.payload)
    
    def enc_password(self, password: str) -> str:
        request = requests.get(constants.LOGIN_URL)
        logging.info("Encrypting password...")
        key_id = int(request.headers["ig-set-password-encryption-web-key-id"])
        logging.debug(f"key_id : {key_id}")
        pub_key = request.headers["ig-set-password-encryption-web-pub-key"]
        logging.debug(f"pub_key : {pub_key}")
        key_version = int(request.headers["ig-set-password-encryption-web-key-version"])
        logging.debug(f"key_version : {key_version}")
        enc_password = encrypt_password(key_id, pub_key, password, key_version)
        logging.debug(f"enc_password : {enc_password}")
        logging.info("Password encrypted")
        return enc_password
    
    def get_csrftoken(self) -> str:
        request = requests.get(constants.BASED_URL)
        soup = BeautifulSoup(request.text, "html.parser")
        script = soup.findAll("script", {"type": "text/javascript"})[3].text
        raw_data = script.replace(";", "").replace("window._sharedData = ", "")
        json_data = json.loads(raw_data)
        csrftoken = json_data["config"]["csrf_token"]
        logging.debug(f"csrftoken : {csrftoken}")
        logging.info("csrftoken retrieved")
        return csrftoken
    
    def get_mid(self) -> str:
        request = requests.get(constants.MID_URL)
        mid = request.text
        logging.debug(f"mid : {mid}")
        logging.info("mid retrieved")
        return mid
    
    def login(self, payload: dict) -> requests.Session:
        login_request = self.session.post(constants.LOGIN_URL, data=payload, allow_redirects=True)
        logging.debug("Login request sent")
        logging.debug(f"LOGIN REQUEST STATUS CODE : {self.login_request.status_code}")
        logging.info(f"LOGIN REQUEST TEXT : {self.login_request.text}\n")
        return login_request

    def get_session(self) -> requests.Session:
        return self.session


if __name__ == "__main__":
    print(InstagramAuth("username", "password").get_session())